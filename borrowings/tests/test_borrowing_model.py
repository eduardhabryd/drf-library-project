from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import datetime, timedelta
from borrowings.models import Borrowing
from books.models import Book


class BorrowingModelTests(TestCase):
    def test_create_borrowing(self):
        book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=10, daily_fee=10.00
        )

        user = get_user_model().objects.create_user(email="test@example.com", password="testpassword")

        borrowing = Borrowing(
            borrow_date=datetime.now().date(),
            expected_return_date=(datetime.now() + timedelta(days=1)).date(),
            actual_return_date=(datetime.now() + timedelta(days=2)).date(),
            book=book,
            user=user,
        )
        borrowing.save()

        saved_borrowing = Borrowing.objects.get(pk=borrowing.pk)

        self.assertEqual(saved_borrowing.borrow_date, datetime.now().date())
        self.assertEqual(saved_borrowing.expected_return_date, (datetime.now() + timedelta(days=1)).date())
        self.assertEqual(saved_borrowing.actual_return_date, (datetime.now() + timedelta(days=2)).date())
        self.assertEqual(saved_borrowing.book, book)
        self.assertEqual(saved_borrowing.user, user)

        self.assertIsNotNone(saved_borrowing.borrow_date)
