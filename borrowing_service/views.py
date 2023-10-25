from rest_framework import viewsets
from .serializers import BorrowingSerializer, BorrowingDetailSerializer

from .models import Borrowing


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        else:
            return BorrowingSerializer
