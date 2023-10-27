from django.urls import path, include
from rest_framework import routers

from borrowings.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("borrowing", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "borrowing/<int:pk>/return-book/",
        BorrowingViewSet.as_view({"post": "return_book"}),
        name="return-book",
    ),
]

app_name = "borrowing"
