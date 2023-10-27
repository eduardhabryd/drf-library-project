from .base_test import BaseTest


class PaymentModelTest(BaseTest):
    def test_payment_creation(self):
        self.assertEqual(self.payment.status_payment, "PENDING")
        self.assertEqual(self.payment.type_payment, "PAYMENT")
        self.assertEqual(self.payment.borrowing, self.borrowing)
        self.assertEqual(self.payment.session_url, "http://test.com")
        self.assertEqual(self.payment.session_id, "123")
        self.assertEqual(self.payment.money, 100.00)
