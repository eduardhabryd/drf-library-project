import stripe
from django.conf import settings

from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment


def create_checkout_session(domain_url, borrowing_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    borrowing = Borrowing.objects.get(pk=borrowing_id)
    book = Book.objects.get(pk=borrowing.book.id)
    book_name = book.title
    days = borrowing.expected_return_date - borrowing.borrow_date
    days = days.days
    price = int(book.daily_fee * 100 * days)

    checkout_session = stripe.checkout.Session.create(
        success_url=domain_url
        + "api/stripe_pay/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=domain_url + "api/stripe_pay/cancel/",
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": book_name,
                    },
                    "unit_amount": price,
                },
                "quantity": 1,
            }
        ]
    )
    Payment.objects.create(
        status_payment="PEN",
        type_payment="PAY",
        borrowing=borrowing,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money=price / 100,
    )
    return checkout_session["id"]


def create_checkout_session_fine(domain_url, borrowing_id, fine_multiplier):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    borrowing = Borrowing.objects.get(pk=borrowing_id)
    book = Book.objects.get(pk=borrowing.book.id)
    book_name = book.title
    days = borrowing.actual_return_date - borrowing.expected_return_date
    days = days.days
    price = int(book.daily_fee * 100 * days * fine_multiplier)
    checkout_session = stripe.checkout.Session.create(
        success_url=domain_url
        + "api/stripe_pay/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=domain_url + "api/stripe_pay/cancel/",
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"Pay fine for {book_name}",
                    },
                    "unit_amount": price,
                },
                "quantity": 1,
            }
        ]
    )
    Payment.objects.create(
        status_payment="PEN",
        type_payment="FIN",
        borrowing=borrowing,
        session_url=checkout_session.url,
        session_id=checkout_session.id,
        money=price / 100,
    )
    return checkout_session["id"]
