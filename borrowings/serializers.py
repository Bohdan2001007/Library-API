from django.shortcuts import get_object_or_404
from rest_framework import serializers
from books.models import Book
from user.serializers import UserSerializer
from .models import Borrowing
from user.models import User


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = ['borrow_date', 'expected_return_date', 'actual_return_date', 'book', 'client', 'is_active']


class BorrowingCreateSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()
    client_id = serializers.IntegerField()

    class Meta:
        model = Borrowing
        fields = ['borrow_date', 'expected_return_date', 'actual_return_date', 'book_id', 'client_id']

    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        book = Book.objects.get(id=book_id)
        book.inventory -= 1
        book.save()
        client_id = validated_data.pop('client_id')
        client = get_object_or_404(User, id=client_id)
        borrowing = Borrowing.objects.create(book=book, client=client, **validated_data)
        return borrowing
