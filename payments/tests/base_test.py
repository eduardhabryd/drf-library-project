import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from payments.models import Payment
from borrowings.models import Borrowing
from books.models import Book


class BaseTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@email.com",
            password="12345"
        )
        self.create_payment()

    def create_payment(self):
        self.book = Book.objects.create(
            title="Some title",
            author="Some author",
            cover=Book.Covers.HARD,
            inventory=10,
            daily_fee=5.00
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today()
        )
        self.payment = Payment.objects.create(
            status_payment="PENDING",
            type_payment="PAYMENT",
            borrowing=self.borrowing,
            session_url="http://test.com",
            session_id="123",
            money=100.00
        )