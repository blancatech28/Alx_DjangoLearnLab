# accounts/serializers.py
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate



class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user (signup).
    """
    password = serializers.CharField(write_only=True, min_length=6)
    username = serializers.CharField(required=True, max_length=15)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value


    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """
    Serializer for logging in a user using email and password.
    Checks invalid credentials and inactive accounts.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("This account is inactive.")
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError("Email and password are required.")


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user profile information.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'bio','followers']






class UpdateUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'bio']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, value):
        user = self.instance
        if CustomUser.objects.filter(email__iexact=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_username(self, value):
        user = self.instance
        if CustomUser.objects.filter(username__iexact=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value


    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance 
    