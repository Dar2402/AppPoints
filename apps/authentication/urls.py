from django.urls import path
from .views import LoginView, CustomTokenRefreshView, UserCreateView
from apps.user_app.views import LogoutView


urlpatterns = [
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(), name='user_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]
