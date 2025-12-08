from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, UpdateUserProfileSerializer
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import generics

User = get_user_model()

class ProfileView(generics.RetrieveUpdateAPIView):
    """
    ViewSet for viewing and editing user profiles.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateUserProfileSerializer
        return UserProfileSerializer 

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    
class RegisterView(generics.CreateAPIView):
    """POST /account/register/ - create a new user"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """POST /auth/login/ - authenticate user and return token"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Explicit token creation (safe even if signals fail)
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserProfileSerializer(user, context={"request": request}).data

        return Response({
            "token": token.key,
            "user": user_data,
            "message": f"Welcome back, {user.username}!"
        }, status=status.HTTP_200_OK)


# Create your views here.
