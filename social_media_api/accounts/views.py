from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from notifications.utils import create_notification


from .models import CustomUser, User
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
)


# ------------------ Register ------------------
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------ Login ------------------
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "token": token.key,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------ Profile ------------------
class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# ------------------ Follow ------------------
class FollowUserView(generics.GenericAPIView):
    """
    POST /follow/<user_id>/
    Authenticated user follows another user.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  

    def post(self, request, user_id):
        try:
            target_user = self.get_queryset().get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.add(target_user)
        return Response(
            {"detail": f"You are now following {target_user.username}."},
            status=status.HTTP_200_OK,
        )


# ------------------ Unfollow ------------------
class UnfollowUserView(generics.GenericAPIView):
    """
    POST /unfollow/<user_id>/
    Authenticated user unfollows another user.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  

    def post(self, request, user_id):
        try:
            target_user = self.get_queryset().get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.remove(target_user)
        return Response(
            {"detail": f"You have unfollowed {target_user.username}."},
            status=status.HTTP_200_OK,
        )
    

