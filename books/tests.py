from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from books.models import Book
from borrowings.models import Borrowing
from user.models import User
from .serializers import BookSerializer


class TestBorrowingModel(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", email="test@example.com", password="test_password",
                                             first_name="Test", last_name="User")
        self.book = Book.objects.create(title="Test Book", author="Test Author", cover="H", inventory=5, Dailyfee=1.0)
        self.borrowing = Borrowing.objects.create(book=self.book, client=self.user, expected_return_date="2023-04-01")

        self.book.client.add(self.user)
        self.book.borrowings.add(self.borrowing)

    def test_str(self):
        self.assertEqual(str(self.book), 'Test Book')


class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            cover='H',
            inventory=5,
            Dailyfee=1.0
        )

    def test_book_serializer(self):
        serializer = BookSerializer(instance=self.book)
        expected_data = {
            'id': self.book.id,
            'title': 'Test Book',
            'author': 'Test Author',
            'cover': 'H',
            'inventory': 5,
            'Dailyfee': '1.00',
            'client': [],
            'borrowings': []
        }
        self.assertEqual(serializer.data, expected_data)


class BookTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", email="test@example.com", password="test_password",
                                             first_name="Test", last_name="User")
        self.book = Book.objects.create(title="Test Book", author="Test Author", cover="H", inventory=5, Dailyfee=1.0)
        self.borrowing = Borrowing.objects.create(book=self.book, client=self.user, expected_return_date="2023-04-01")
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        self.book.client.add(self.user)
        self.book.borrowings.add(self.borrowing)

    def test_list_books(self):
        url = reverse('books:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        url = reverse('books:book-list')
        data = {'title': 'New Book', 'author': 'New Author', 'cover': 'P', 'inventory': 3, 'Dailyfee': 2.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        url = reverse('books:book-detail-api', args=[self.book.id])
        data = {'title': 'Updated Book'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book(self):
        url = reverse('books:book-detail-api', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book(self):
        url = reverse('books:book-detail-api', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['author'], 'Test Author')
        self.assertEqual(response.data['cover'], 'H')
        self.assertEqual(response.data['inventory'], 5)
        self.assertEqual(response.data['Dailyfee'], '1.00')
