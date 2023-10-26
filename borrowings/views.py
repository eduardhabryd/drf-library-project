from django.db import transaction
from rest_framework import viewsets

from books.models import Book
from .serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)

from .models import Borrowing


class BorrowingViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        user = self.request.user

        if not user.is_staff:
            queryset = queryset.filter(user=user)

        return queryset

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
