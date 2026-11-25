"""Authentication endpoints."""
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserSerializer


@extend_schema(tags=["auth"], summary="Register a candidate or employer account")
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["auth"], summary="Log in with email and password, returns access and refresh tokens")
class LoginView(TokenObtainPairView):
    pass


@extend_schema(tags=["auth"], summary="Get a new access token from a refresh token")
class RefreshView(TokenRefreshView):
    pass


@extend_schema(tags=["auth"], summary="Details of the logged-in user")
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
