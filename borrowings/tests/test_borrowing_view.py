from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowings.models import Borrowing


BORROWING_URL = reverse("borrowings:borrowing-list")


def sample_borrowing(**params):
    user = get_user_model().objects.create_user(
        email="active@test.com",
        password="testpass",
    )
    book = Book.objects.create(
        title="Active Book",
        author="Active Author",
        inventory=1,
        daily_fee=10.00,
    )
    defaults = {
        "user": user,
        "book": book,
        "expected_return_date": "2023-11-01",
    }
    defaults.update(params)
    return Borrowing.objects.create(**defaults)


class BorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com", password="testpassword"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=1,
            daily_fee=10.00,
        )
        self.url = reverse("borrowings:borrowing-list")
        self.client.force_authenticate(user=self.user)

    # def test_create_borrowing(self):
    #     data = {
    #         "borrow_date": datetime.now().date(),
    #         "expected_return_date": datetime.now().date() + timedelta(days=3),
    #         "book": self.book.pk,
    #     }
    #
    #     response = self.client.post(self.url, data, format="json")
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Borrowing.objects.count(), 1)
    #
    #     borrowing = Borrowing.objects.get()
    #     self.assertEqual(borrowing.user, self.user)
    #     self.assertEqual(borrowing.book, self.book)
    #     self.assertEqual(
    #         str(borrowing.expected_return_date),
    #         str(date.today() + timedelta(days=3)),
    #     )
    #     self.assertIsNone(borrowing.actual_return_date)

    def test_borrow_nonexistent_book(self):
        data = {"book": 999, "expected_return_date": "2023-11-01"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Borrowing.objects.count(), 0)

    def test_borrow_unavailable_book(self):
        self.book.inventory = 0
        self.book.save()

        data = {"book": self.book.id, "expected_return_date": "2023-11-01"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Borrowing.objects.count(), 0)


class UnauthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedMovieApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="testpass",
        )
        self.client.force_authenticate(self.admin_user)

    def test_filter_active_borrowings(self):
        sample_borrowing()

        inactive_book = Book.objects.create(
            title="Inactive Book",
            author="Inactive Author",
            inventory=1,
            daily_fee=10.00,
        )
        Borrowing.objects.create(
            user=self.admin_user,  # Using admin user for simplicity
            book=inactive_book,
            expected_return_date="2023-11-05",
            actual_return_date="2023-11-03",
        )

        url = BORROWING_URL + "?is_active=true"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_borrowings_by_user(self):
        sample_borrowing()
        user2 = get_user_model().objects.create_user(
            email="user2@test.com",
            password="testpass",
        )
        book2 = Book.objects.create(
            title="Test book",
            author="Test buthor",
            inventory=1,
            daily_fee=10.00,
        )
        Borrowing.objects.create(
            user=user2,
            book=book2,
            expected_return_date="2023-11-05",
        )

        url = BORROWING_URL + f"?user_id={self.admin_user.id}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AdminBorrowingViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@test.com",
            password="testpass",
        )
        self.client.force_authenticate(self.admin_user)

    def test_filter_user_borrowings_by_id(self):
        sample_borrowing()
        user2 = get_user_model().objects.create_user(
            email="user2@test.com",
            password="testpass",
        )
        book2 = Book.objects.create(
            title="Test book",
            author="Test author",
            inventory=1,
            daily_fee=10.00,
        )
        Borrowing.objects.create(
            user=user2,
            book=book2,
            expected_return_date="2023-11-05",
        )

        url = BORROWING_URL + f"?user_id={self.admin_user.id}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class ReturnBookTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.borrowing = sample_borrowing()
        self.user = self.borrowing.user
        self.book = self.borrowing.book
        self.client.force_authenticate(self.user)

    def test_return_book(self):
        response = self.client.post(
            reverse(
                "borrowing:return-book",
                kwargs={"pk": self.borrowing.id}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"status": "Book returned"}
        )
        self.borrowing.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 2)
