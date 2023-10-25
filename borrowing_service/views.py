from rest_framework import viewsets
from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        else:
            return BorrowingSerializer
