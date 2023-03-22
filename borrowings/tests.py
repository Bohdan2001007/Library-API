import datetime
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingCreateSerializer
from user.models import User


class TestBorrowingModel(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", email="test@example.com", password="test_password",
                                             first_name="Test", last_name="User")
        self.book = Book.objects.create(title="Test Book", author="Test Author", cover="H", inventory=5, Dailyfee=1.0)
        self.borrowing = Borrowing.objects.create(book=self.book, client=self.user, expected_return_date="2023-04-01")

    def test_str(self):
        expected_result =\
            f"{self.borrowing.borrow_date} - {self.borrowing.expected_return_date} - {self.borrowing.actual_return_date}"
        self.assertEqual(str(self.borrowing), expected_result)


class BorrowingSerializerTestCase(TestCase):
    def setUp(self):
        self.client = User.objects.create(username="test_user", email="test@example.com", is_staff=False)
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", cover="H", inventory=5, Dailyfee=1.0
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book, client=self.client, expected_return_date="2023-04-01"
        )
        self.borrowing.refresh_from_db()

    def test_borrowing_serializer(self):
        borrowing_serializer = BorrowingSerializer(self.borrowing)

        expected_data = {
            'borrow_date': self.borrowing.borrow_date.strftime('%Y-%m-%d'),
            'expected_return_date': '2023-04-01',
            'actual_return_date': None,
            'book': self.book.id,
            'client': [
                ('id', self.client.id),
                ('username', 'test_user'),
                ('email', 'test@example.com'),
                ('first_name', ''),
                ('last_name', ''),
                ('is_staff', False),
            ],
            'is_active': True
        }

        self.assertEqual(borrowing_serializer.data, expected_data)

    def test_borrowing_create_serializer(self):
        borrowing_create_serializer = BorrowingCreateSerializer(data={
            'book_id': self.book.id,
            'client_id': self.client.id,
            'expected_return_date': '2023-04-10',
        })

        self.assertTrue(borrowing_create_serializer.is_valid())
        created_borrowing = borrowing_create_serializer.save()

        self.assertEqual(created_borrowing.book, self.book)
        self.assertEqual(created_borrowing.client, self.client)
        self.assertEqual(created_borrowing.expected_return_date.strftime('%Y-%m-%d'), '2023-04-10')

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)


class BorrowingListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", email="test@example.com", password="test_password",
                                             first_name="Test", last_name="User")
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", cover="H", inventory=5, Dailyfee=1.0
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book, client=self.user, expected_return_date="2023-04-01"
        )
        self.url = reverse('borrowing-list-create')

    def test_get_borrowings_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_borrowing(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'book_id': self.book.id,
            'client_id': self.user.id,
            'expected_return_date': '2023-04-10',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BorrowingDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", email="test@example.com", password="test_password",
                                             first_name="Test", last_name="User")
        self.book = Book.objects.create(title="Test Book", author="Test Author", cover="H", inventory=5, Dailyfee=1.0)
        self.borrowing = Borrowing.objects.create(book=self.book, client=self.user, expected_return_date="2023-04-01")
        self.url = reverse('borrowing-detail', kwargs={'pk': self.borrowing.pk})

    def test_get_borrowing_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        borrowing = Borrowing.objects.get(pk=self.borrowing.pk)
        self.assertEqual(borrowing.book.title, 'Test Book')
        self.assertEqual(response.data['client']['email'], 'test@example.com')

    def test_update_borrowing(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'actual_return_date': datetime.now().strftime('%Y-%m-%d'),
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['actual_return_date'])

    def test_delete_borrowing(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Borrowing.objects.filter(pk=self.borrowing.pk).exists())
