from django.db import models

from borrowings.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = (("PEN", "PENDING"), ("PAI", "PAID"))
    TYPE_CHOICES = (("PAY", "PAYMENT"), ("FIN", "FINE"))

    status_payment = models.CharField(max_length=7, choices=STATUS_CHOICES)
    type_payment = models.CharField(max_length=7, choices=TYPE_CHOICES)
    borrowing = models.OneToOneField(
        Borrowing,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money = models.DecimalField(max_digits=5, decimal_places=2)
