from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from django.db.models import Sum
from django.contrib.auth import get_user_model
from apps.authentication.serializers import UserSerializer
from .serializers import TaskSerializer
from .models import Task

# Create your views here.

User = get_user_model()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve the current user's data.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """
        Update the current user's data.
        """
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def calculate_points_by_category(self, request, *args, **kwargs):
        category_name = request.query_params.get('category')
        if not category_name:
            return Response({"error": "category query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        total_points = Task.objects.filter(app__category__name=category_name).aggregate(total_points=Sum('points'))['total_points'] or 0
        return Response({"total_points": total_points})

    def calculate_points_by_subcategory(self, request, *args, **kwargs):
        subcategory_name = request.query_params.get('subcategory')
        if not subcategory_name:
            return Response({"error": "subcategory query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        total_points = Task.objects.filter(app__subcategory__name=subcategory_name).aggregate(total_points=Sum('points'))['total_points'] or 0
        return Response({"total_points": total_points})

    def calculate_points_by_user(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({"error": "user_id query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        total_points = Task.objects.filter(user_id=user_id).aggregate(total_points=Sum('points'))['total_points'] or 0
        return Response({"total_points": total_points})

    def list(self, request, *args, **kwargs):
        if 'category' in request.query_params:
            return self.calculate_points_by_category(request, *args, **kwargs)
        elif 'subcategory' in request.query_params:
            return self.calculate_points_by_subcategory(request, *args, **kwargs)
        elif 'user_id' in request.query_params:
            return self.calculate_points_by_user(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)