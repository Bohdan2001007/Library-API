from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Book
from .permissions import IsAdminOrReadOnly
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
        Perform CRUD operations on books.

        - Retrieve a list of all books or a single book by its id.
        - Create, update, or delete a book (only available to admin users).
        - Authenticated users will see all books.
        - Unauthenticated users will only see books with inventory greater than 0.
    """
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
