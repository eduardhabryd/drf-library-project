from django.test import TestCase

from books.models import Book


class ModelTests(TestCase):
    def test_book_str(self):
        book = Book.objects.create(
            title="Test",
            author="Test Author",
            cover="Hard",
            inventory=10,
            daily_fee=10.99,
        )
        self.assertEqual(str(book), f"{book.title} ({book.inventory})")
