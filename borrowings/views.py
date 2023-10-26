from django.db import transaction
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from books.models import Book
from .serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)

from .models import Borrowing


class BorrowingViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        user = self.request.user
        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", None)

        if not user.is_staff:
            queryset = queryset.filter(user=user)
        else:
            if user_id:
                queryset = queryset.filter(user_id=user_id)

        if is_active.lower() == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)

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
