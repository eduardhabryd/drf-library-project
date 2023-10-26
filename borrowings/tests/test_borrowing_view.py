from datetime import datetime, timedelta, date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing


class BorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com", password="testpassword"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=1,
            daily_fee=10.00,
        )
        self.url = reverse("borrowings:borrowing-list")

    def test_create_borrowing(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "borrow_date": datetime.now().date(),
            "expected_return_date": datetime.now().date() + timedelta(days=3),
            "book": self.book.pk,
        }

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Borrowing.objects.count(), 1)

        borrowing = Borrowing.objects.get()
        self.assertEqual(borrowing.user, self.user)
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(
            str(borrowing.expected_return_date),
            str(date.today() + timedelta(days=3)),
        )
        self.assertIsNone(borrowing.actual_return_date)

    def test_borrow_nonexistent_book(self):
        data = {"book": 999, "expected_return_date": "2023-11-01"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Borrowing.objects.count(), 0)

    def test_borrow_unavailable_book(self):
        self.book.inventory = 0
        self.book.save()

        data = {"book": self.book.id, "expected_return_date": "2023-11-01"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Borrowing.objects.count(), 0)
