from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileView, LogoutView, UserTaskViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'tasks', UserTaskViewSet, basename='user-task')

urlpatterns = [
    path('', include(router.urls)),
    path('me/', UserProfileView.as_view(), name='user-me'),
]
