import asyncio

from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.bot_service.bot import successful_notification_handler
from payments.models import Payment
from .stripe_services import (
    create_checkout_session as create_stripe_checkout_session,
    create_checkout_session_fine as create_stripe_checkout_session_fine
)


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
        try:
            session_id = create_stripe_checkout_session(
                domain_url, borrowing_id
            )
            return JsonResponse({"sessionId": session_id})
        except Exception as e:
            return JsonResponse({"error": str(e)})


FINE_MULTIPLIER = 2


@csrf_exempt
def create_checkout_session_fine(request, borrowing_id=None):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        try:
            session_id = create_stripe_checkout_session_fine(
                domain_url, borrowing_id, FINE_MULTIPLIER
            )
            return JsonResponse({"sessionId": session_id})
        except Exception as e:
            return JsonResponse({"error": str(e)})


@api_view(["GET"])
def success_view(request):
    session_id = request.query_params.get("session_id")
    payment = Payment.objects.get(session_id=session_id)
    payment.status_payment = "PAI"
    payment.save()

    borrowing = payment.borrowing
    str(borrowing)
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
