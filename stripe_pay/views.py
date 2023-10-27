import asyncio

import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.bot_service.bot import successful_notification_handler
from borrowings.models import Borrowing
from books.models import Book
from payments.models import Payment


class PayView(TemplateView):
    template_name = "pay.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowing_id = self.kwargs.get("borrowing_id")
        context["borrowing_id"] = borrowing_id
        return context


class PayFineView(TemplateView):
    template_name = "pay_fine.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowing_id = self.kwargs.get("borrowing_id")
        context["borrowing_id"] = borrowing_id
        return context


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, borrowing_id=None):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        borrowing = Borrowing.objects.get(pk=borrowing_id)
        book = Book.objects.get(pk=borrowing.book.id)
        book_name = book.title
        days = borrowing.expected_return_date - borrowing.borrow_date
        days = days.days
        price = int(book.daily_fee * 100 * days)
        try:
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
                ],
            )
            Payment.objects.create(
                status_payment="PEN",
                type_payment="PAY",
                borrowing=borrowing,
                session_url=checkout_session.url,
                session_id=checkout_session.id,
                money=price / 100,
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


FINE_MULTIPLIER = 2


@csrf_exempt
def create_checkout_session_fine(request, borrowing_id=None):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        borrowing = Borrowing.objects.get(pk=borrowing_id)
        book = Book.objects.get(pk=borrowing.book.id)
        book_name = book.title
        days = borrowing.actual_return_date - borrowing.expected_return_date
        days = days.days
        price = int(book.daily_fee * 100 * days * FINE_MULTIPLIER)
        try:
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
                ],
            )
            Payment.objects.create(
                status_payment="PEN",
                type_payment="FIN",
                borrowing=borrowing,
                session_url=checkout_session.url,
                session_id=checkout_session.id,
                money=price / 100,
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@api_view(["GET"])
def success_view(request):
    session_id = request.query_params.get("session_id")
    payment = Payment.objects.get(session_id=session_id)
    payment.status_payment = "PAI"
    payment.save()

    borrowing = payment.borrowing
    asyncio.run(successful_notification_handler(borrowing))

    return Response({"status": "success"})


@api_view(["GET"])
def cancelled_view(request):
    return Response(
        {
            "status": "payment canceled, but you can pay a bit later, "
            "(but the session is available for only 24h)"
        }
    )
