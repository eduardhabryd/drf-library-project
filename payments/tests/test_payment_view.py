from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from payments.tests.base_test import BaseTest


class PaymentViewSetTest(BaseTest, APITestCase):
    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_superuser(
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
