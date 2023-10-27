from django.urls import path

from stripe_pay.views import PayView, stripe_config, create_checkout_session

urlpatterns = [
    path("pay/<int:borrowing_id>/", PayView.as_view(), name="pay"),
    path("config/", stripe_config),
    path(
        "create-checkout-session/<int:borrowing_id>/",
        create_checkout_session,
        name="create-checkout-session"
    ),
]

app_name = "stripe_pay"
