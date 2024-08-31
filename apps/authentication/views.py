from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from .serializers import TokenSerializer, UserSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserPointsView(APIView):
    
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
