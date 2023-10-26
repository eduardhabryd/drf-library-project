import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from borrowings.models import Borrowing
from books.models import Book
from payments.models import Payment


class PayView(TemplateView):
    template_name = "pay.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowing_id = self.kwargs.get('borrowing_id')
        context['borrowing_id'] = borrowing_id
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
                + "success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': book_name,
                            },
                            'unit_amount': price,
                        },
                        'quantity': 1,
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
