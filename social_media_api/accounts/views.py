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



from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser

class DevelopView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def follow_user(self, request, user_id):
        """
        Follow another user
        """
        target_user = get_object_or_404(CustomUser.objects.all(), id=user_id)
        if target_user == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.followers.add(target_user)
        return Response({"detail": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)

    def unfollow_user(self, request, user_id):
        """
        Unfollow another user
        """
        target_user = get_object_or_404(CustomUser.objects.all(), id=user_id)
        if target_user == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.followers.remove(target_user)
        return Response({"detail": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)


# Create your views here.
