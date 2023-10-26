import asyncio

from django.db import transaction
from rest_framework import viewsets

from app.bot_service.bot import borrowing_creation_handler
from books.models import Book
from .serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)

from .models import Borrowing


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        else:
            return BorrowingSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            book_pk = serializer.validated_data["book"].pk
            book = Book.objects.get(pk=book_pk)
            book.inventory -= 1
            book.save()
            serializer.save(user=self.request.user)

        borrowing = Borrowing.objects.last()
        str(borrowing)
        asyncio.run(borrowing_creation_handler(borrowing))
