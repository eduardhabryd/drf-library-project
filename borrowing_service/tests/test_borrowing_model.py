from datetime import timezone
from unittest import TestCase

from rest_framework import status

from books.models import Book
from borrowing_service.models import Borrowing
from rest_framework.test import APIClient

from borrowing_service.serializers import BorrowingDetailSerializer, BorrowingSerializer


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="Testuser")
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=5
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date=timezone.now(),
            expected_return_date=timezone.now() + timezone.timedelta(days=7),
            book_id=self.book,
            user_id=self.user,
        )

    def test_str_representation(self):
        expected_str = (
            f"Borrowed Book ID: {self.book.id}, "
            f"User ID: {self.user.id}, "
            f"Borrow Date: {self.borrowing.borrow_date}, "
            f"Expected Return Date: {self.borrowing.expected_return_date}, "
            f"Actual Return Date: {self.borrowing.actual_return_date}"
        )
        self.assertEqual(str(self.borrowing), expected_str)


class BorrowingViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="Testuser", password="testpassword")
        self.borrowing = Borrowing.objects.create(
            borrow_date="2023-10-15",
            expected_return_date="2023-10-22",
            book_id=1,
            user_id=self.user,
        )

    def test_list_view_serializer(self):
        response = self.client.get("/api/borrowings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BorrowingSerializer(self.borrowing).data)

    def test_detail_view_serializer(self):
        response = self.client.get(f"/api/borrowings/{self.borrowing.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, BorrowingDetailSerializer(self.borrowing).data)

    def test_dates_representation(self):
        self.assertEqual(
            str(self.borrowing.borrow_date), str(self.borrowing.borrow_date)
        )
        self.assertEqual(
            str(self.borrowing.expected_return_date),
            str(self.borrowing.expected_return_date),
        )
        self.assertEqual(
            str(self.borrowing.actual_return_date),
            str(self.borrowing.actual_return_date),
        )

        self.assertTrue(
            self.borrowing.borrow_date < self.borrowing.expected_return_date
        )

        self.assertTrue(self.borrowing.actual_return_date > self.borrowing.borrow_date)
