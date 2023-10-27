from django.db import models
from rest_framework.exceptions import ValidationError

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrowings"
    )

    def __str__(self):
        return (
            f"Borrowed Book ID: {self.book},"
            f" User ID: {self.user}, "
            f"Borrow Date: {self.borrow_date}, "
            f"Expected Return Date: {self.expected_return_date}, "
            f"Actual Return Date: {self.actual_return_date}"
        )

    def clean(self):
        if self.expected_return_date < self.borrow_date:
            raise ValidationError(
                "Expected return date cannot be earlier than the borrow date."
            )
        if self.actual_return_date and (
            self.actual_return_date < self.borrow_date
            or self.actual_return_date > self.expected_return_date
        ):
            raise ValidationError(
                "Actual return date must be between "
                "borrow date and expected return date."
            )

    def is_returned(self):
        return self.actual_return_date is not None
