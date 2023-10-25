from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import date
from borrowings.models import Borrowing
from books.models import Book
from users.models import User


class BorrowingModelTests(TestCase):
    def test_create_borrowing(self):
        book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=10, daily_fee=10.00
        )

        user = get_user_model().objects.create_user(email="test@example.com", password="testpassword")

        borrowing = Borrowing(
            expected_return_date=date(2023, 11, 12),
            actual_return_date=date(2023, 11, 11),
            book_id=book,
            user_id=user,
        )
        borrowing.save()

        saved_borrowing = Borrowing.objects.get(pk=borrowing.pk)

        self.assertEqual(saved_borrowing.expected_return_date, date(2023, 11, 12))
        self.assertEqual(saved_borrowing.actual_return_date, date(2023, 11, 11))
        self.assertEqual(saved_borrowing.book_id, book)
        self.assertEqual(saved_borrowing.user_id, user)

        self.assertIsNotNone(saved_borrowing.borrow_date)
