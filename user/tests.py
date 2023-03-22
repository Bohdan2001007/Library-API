from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import serializers
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from .serializers import UserSerializer, AuthTokenSerializer
User = get_user_model()


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            username='test_user',
            password='test_password',
            first_name='Test',
            last_name='User'
        )

        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('test_password'))

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            password='super_password',
            first_name='Super',
            last_name='User'
        )

        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertEqual(superuser.username, 'superuser')
        self.assertEqual(superuser.first_name, 'Super')
        self.assertEqual(superuser.last_name, 'User')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password('super_password'))

    def test_normalize_email(self):
        user = User.objects.create_user(
            email='Test@example.com',
            username='test_user',
            password='test_password',
            first_name='Test',
            last_name='User'
        )

        self.assertEqual(user.email, 'Test@example.com')

class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test_user',
            password='test_password',
            first_name='Test',
            last_name='User'
        )
        self.serializer = UserSerializer(instance=self.user)

    def test_user_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {"id", "username", "email", "first_name", "last_name", "is_staff"})

    def test_user_serializer_create(self):
        data = {
            "email": "new_user@example.com",
            "username": "new_user",
            "password": "new_password",
            "first_name": "New",
            "last_name": "User",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "new_user@example.com")
        self.assertEqual(user.username, "new_user")
        self.assertEqual(user.first_name, "New")
        self.assertEqual(user.last_name, "User")
        self.assertTrue(user.check_password("new_password"))

    def test_user_serializer_update(self):
        data = {"password": "new_password"}
        serializer = UserSerializer(self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password("new_password"))


class AuthTokenSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test_user',
            password='test_password',
            first_name='Test',
            last_name='User'
        )
        self.client = APIClient()

    def test_auth_token_serializer_fields(self):
        data = {"email": "test@example.com", "password": "test_password"}
        serializer = AuthTokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_auth_token_serializer_invalid_credentials(self):
        data = {"email": "test@example.com", "password": "wrong_password"}
        serializer = AuthTokenSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_auth_token_serializer_missing_fields(self):
        data = {"email": "test@example.com"}
        serializer = AuthTokenSerializer(data=data)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)


class RegisterUserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user:register_user')

    def test_register_user(self):
        data = {
            "email": "new_user@example.com",
            "username": "new_user",
            "password": "new_password",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(email="new_user@example.com").username, "new_user")


class UserDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test_user',
            password='test_password',
            first_name='Test',
            last_name='User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('user:user_detail')

    def test_user_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["username"], "test_user")

    def test_user_detail_view_update(self):
        data = {"first_name": "Updated"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Updated")