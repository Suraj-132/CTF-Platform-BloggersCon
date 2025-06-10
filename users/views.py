from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import generics, permissions
from .serializers import UserProfileSerializer


from rest_framework_simplejwt.views import TokenObtainPairView
from .throttles import LoginRateThrottle  # Make sure this path matches your file structure

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



User = get_user_model()

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = request.build_absolute_uri(
            reverse('reset-password', args=[user.pk, token])
        )

        # Send email (prints to console)
        send_mail(
            subject='Reset Your Password',
            message=f'Click the link to reset your password: {reset_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request, uid, token):
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('password')
        if not new_password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)



class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class RateLimitedLoginView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]



