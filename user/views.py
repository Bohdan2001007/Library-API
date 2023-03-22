from rest_framework import generics, permissions

from .serializers import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    """
        Create a new user in the system.

        Provide username, email, and password.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
        Retrieve or update user information.

        Authenticated users can retrieve or update their information.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()
