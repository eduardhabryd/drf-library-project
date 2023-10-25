from rest_framework import serializers
from books.models import Book
from .models import Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BorrowingSerializer(serializers.ModelSerializer):
    pass


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_info = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = "__all__"

    def get_book_info(self, obj):
        book = object.book_id
        return BookSerializer(book).data
