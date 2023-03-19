from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Book
from .serializers import BookSerializer
from .permissions import IsAdminOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly] # Change permission class to custom class
    authentication_classes = [JWTAuthentication]  # Add TokenAuthentication

    def get_queryset(self):
        queryset = Book.objects.all()
        if self.request.user.is_authenticated:  # Check if user is authenticated
            if self.request.user.is_staff:  # Check if user is staff member
                return queryset
            else:
                return queryset.filter(inventory__gt=0)  # Only return books with inventory above 0
        else:
            return queryset.filter(inventory__gt=0)  # Only return books with inventory above 0

    def perform_create(self, serializer):
        serializer.save()  # Save new book

    def perform_update(self, serializer):
        serializer.save()  # Update book
