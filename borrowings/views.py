from datetime import datetime
import asyncio

from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        user = self.request.user
        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", None)

        if not user.is_staff:
            queryset = queryset.filter(user=user)
        else:
            if user_id:
                queryset = queryset.filter(user_id=user_id)

        if is_active and is_active.lower() == "true":
            queryset = queryset.filter(actual_return_date__isnull=True)

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        else:
            return BorrowingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        redirect_url = reverse("stripe_pay:pay", args=[serializer.data["id"]])
        return HttpResponseRedirect(redirect_url)

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

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.is_returned():
            return Response(
                {"error": "Book has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.actual_return_date = datetime.now()
        borrowing.save()
        book = borrowing.book
        book.inventory += 1
        book.save()
        if (
            borrowing.actual_return_date.date()
            > borrowing.expected_return_date
        ):
            url = reverse(
                "stripe_pay:pay-fine", kwargs={"borrowing_id": borrowing.id}
            )
            return HttpResponseRedirect(url)

        return Response(
            {"status": "Book has been returned."},
        )
