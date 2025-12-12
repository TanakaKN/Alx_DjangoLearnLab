from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token  

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic serializer to show user info."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "bio", "profile_picture"]


class RegisterSerializer(serializers.ModelSerializer):
    """Handles user registration and token creation."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """Validates login credentials."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        attrs["user"] = user
        return attrs
