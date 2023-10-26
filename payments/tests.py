import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from users.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from payments.models import Payment
from borrowings.models import Borrowing
from books.models import Book


class BaseTest(TestCase):
    def setUp(self):
        self.user = get_user_model().create_user(
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


class PaymentModelTest(BaseTest):
    def test_payment_creation(self):
        self.assertEqual(self.payment.status_payment, "PENDING")
        self.assertEqual(self.payment.type_payment, "PAYMENT")
        self.assertEqual(self.payment.borrowing, self.borrowing)
        self.assertEqual(self.payment.session_url, "http://test.com")
        self.assertEqual(self.payment.session_id, "123")
        self.assertEqual(self.payment.money, 100.00)


class PaymentViewSetTest(BaseTest, APITestCase):
    def setUp(self):
        super().setUp()
        self.admin = get_user_model().create_superuser(
            email="admin@email.com",
            password="12345"
        )
        self.client = APIClient()

    def test_list_payments(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("payment:payment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_payment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse(
            "payment:payment-detail",
            kwargs={"pk": self.payment.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)

    def test_list_payments_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse("payment:payment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
