from rest_framework import serializers

from books.models import Book
from .models import Borrowing
from user.models import User


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ['borrow_date', 'expected_return_date', 'actual_return_date', 'is_active']


class BorrowingCreateSerializer(serializers.ModelSerializer):
    book_ids = serializers.ListField(child=serializers.IntegerField())
    client_ids = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Borrowing
        fields = ['borrow_date', 'expected_return_date', 'actual_return_date', 'book_ids', 'client_ids']

    def create(self, validated_data):
        book_ids = validated_data.pop('book_ids')
        books = Book.objects.filter(id__in=book_ids)

        # Decrease the inventory for each book in the list
        for book in books:
            book.inventory -= 1
            book.save()

        client_ids = validated_data.pop('client_ids')
        clients = User.objects.filter(id__in=client_ids)

        borrowing = Borrowing.objects.create(**validated_data)
        borrowing.book.set(books)
        borrowing.clients.set(clients)
        borrowing.save()

        return borrowing
