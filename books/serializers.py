from rest_framework import serializers

from borrowings.serializers import BorrowingSerializer
from user.serializers import UserSerializer
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    borrowings = BorrowingSerializer(many=True, read_only=True)
    clients = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'cover', 'inventory', 'Dailyfee', 'clients', 'borrowings')
