from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book

BOOK_LIST_URL = reverse("books:book-list")


def get_book_detail_url(book_id):
    return reverse("books:book-detail", args=[book_id])


def sample_book(data: dict) -> Book:
    initial_data = {
        "title": "Test",
        "author": "Test Author",
        "cover": "Hard",
        "inventory": 10,
        "daily_fee": 10.99,
    }
    initial_data.update(**data)
    return Book.objects.create(**initial_data)


class AnonimUserPermissions(TestCase):
    """Anonim Users can only list or retrieve books."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@test.com",
            password="12345678",
        )
        self.client.force_login(self.user)

    def test_anonymous_user_can_list_books(self):
        book = sample_book(data={"title": "Test"})
        book2 = sample_book(data={"title": "Test2"})
        book3 = sample_book(data={"title": "Test3"})

        books = [book, book2, book3]

        response = self.client.get(BOOK_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        response_titles = [book_data["title"] for book_data in response_data]

        for book in books:
            self.assertIn(book.title, response_titles)

    def test_anonymous_user_can_retrieve_book(self):
        book = sample_book(data={"title": "Test123"})

        response = self.client.get(get_book_detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertEqual(response_data["title"], book.title)

    def test_anonymous_user_cannot_create_book(self):
        test_data = {
            "title": "Test",
            "author": "Test Author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 10.99,
        }
        response = self.client.post(BOOK_LIST_URL, data=test_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_update_book(self):
        book = sample_book(data={"title": "Test123"})
        test_data = {
            "title": "Test",
            "author": "Test Author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 10.99,
        }
        response = self.client.put(get_book_detail_url(book.id), data=test_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_delete_book(self):
        book = sample_book(data={"title": "Test123"})
        response = self.client.delete(get_book_detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AdminUserPermissions(TestCase):
    """Admin Users can create, update and delete books."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="testsuperuser@test.com",
            password="12345678",
        )
        self.client.force_authenticate(self.user)

    def test_admin_user_can_create_book(self):
        test_data = {
            "title": "Test",
            "author": "Test Author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 10.99,
        }
        response = self.client.post(BOOK_LIST_URL, data=test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_user_can_update_book(self):
        book = sample_book(data={"title": "Test123"})
        test_data = {
            "title": "Test",
            "author": "Test Author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 10.99,
        }
        response = self.client.put(get_book_detail_url(book.id), data=test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_delete_book(self):
        book = sample_book(data={"title": "Test123"})
        response = self.client.delete(get_book_detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_user_can_list_books(self):
        book = sample_book(data={"title": "Test"})
        book2 = sample_book(data={"title": "Test2"})
        book3 = sample_book(data={"title": "Test3"})

        books = [book, book2, book3]

        response = self.client.get(BOOK_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        response_titles = [book_data["title"] for book_data in response_data]

        for book in books:
            self.assertIn(book.title, response_titles)

    def test_admin_user_can_retrieve_book(self):
        book = sample_book(data={"title": "Test123"})
        response = self.client.get(get_book_detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertEqual(response_data["title"], book.title)


class AuthenticatedUserPermissions(TestCase):
    """Authenticated Users can create, update and delete books."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@test.com",
            password="12345678",
        )
        self.client.force_authenticate(self.user)

    def test_authenticated_user_cant_create_book(self):
        test_data = {
            "title": "Test",
            "author": "Test Author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 10.99,
        }
        response = self.client.post(BOOK_LIST_URL, data=test_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cant_delete_book(self):
        book = sample_book(data={"title": "Test123"})
        response = self.client.delete(get_book_detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_list_books(self):
        book = sample_book(data={"title": "Test"})
        book2 = sample_book(data={"title": "Test2"})
        book3 = sample_book(data={"title": "Test3"})

        books = [book, book2, book3]

        response = self.client.get(BOOK_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        response_titles = [book_data["title"] for book_data in response_data]

        for book in books:
            self.assertIn(book.title, response_titles)

    def test_authenticated_user_can_retrieve_book(self):
        book = sample_book(data={"title": "Test123"})
        response = self.client.get(get_book_detail_url(book.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertEqual(response_data["title"], book.title)

    def test_authenticated_user_cant_update_book(self):
        book = sample_book(data={"title": "Test123"})
        test_data = {
            "title": "Test",
            "author": "Test Author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 10.99,
        }
        response = self.client.put(get_book_detail_url(book.id), data=test_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
