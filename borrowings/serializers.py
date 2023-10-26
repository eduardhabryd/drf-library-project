from datetime import datetime

from rest_framework import serializers
from books.models import Book
from .models import Borrowing

from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_info = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = "__all__"

    def get_book_info(self, obj):
        book = obj.book
        return BookSerializer(book).data


class BorrowingCreateSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(many=False, slug_field="id", queryset=Book.objects.all())
    expected_return_date = serializers.DateField()
    actual_return_date = serializers.DateField(
        read_only=True, default=None, allow_null=True
    )

    class Meta:
        model = Borrowing
        fields = ("id", "book", "expected_return_date", "actual_return_date")

    def validate(self, attrs):
        data = super().validate(attrs)

        print(data)
        book_pk = data.get("book").pk
        print(book_pk)
        try:
            book = Book.objects.get(pk=book_pk)
        except Book.DoesNotExist:
            raise serializers.ValidationError(
                "Book not found!"
            )

        if int(book.inventory) <= 0:
            raise serializers.ValidationError(
                "There are no copies of the book available for borrowing"
            )

        expected_return_date = data.get("expected_return_date")
        current_date = datetime.now().date()

        if expected_return_date <= current_date:
            raise serializers.ValidationError(
                "Expected return date should be in the future."
            )

        return data
