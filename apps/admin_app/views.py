from django.shortcuts import render
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Category, Subcategory, App
from .serializers import CategorySerializer, SubcategorySerializer, AppSerializer
from apps.authentication import permissions
from ..user_app import models as user_app_models
from ..user_app import serializers as user_app_serializers

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]  
        else:
            permission_classes = [IsAdminUser] 
        return [permission() for permission in permission_classes]

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]  
        else:
            permission_classes = [IsAdminUser] 
        return [permission() for permission in permission_classes]


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    
    def perform_create(self, serializer):
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to add the app.")
        
        serializer.save(created_by=self.request.user)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]  
        else:
            permission_classes = [IsAdminUser] 
        return [permission() for permission in permission_classes]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = user_app_models.Task.objects.all()
    serializer_class =user_app_serializers.TaskSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def calculate_points_by_user(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        if not user_id:
            return Response({"error": "user_id query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        total_points = user_app_models.Task.objects.filter(user_id=user_id).aggregate(total_points=Sum('points'))['total_points'] or 0
        return Response({"total_points": total_points})

    def list(self, request, *args, **kwargs):
        if 'user_id' in request.query_params:
            return self.calculate_points_by_user(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)