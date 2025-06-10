from django.urls import path
from .views import UserRegistrationView, ForgotPasswordView, ResetPasswordView, UserProfileView, RateLimitedLoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', RateLimitedLoginView.as_view(), name='login'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<int:uid>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]


    
