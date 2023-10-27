from django.urls import path

from stripe_pay.views import PayView, stripe_config, create_checkout_session, success_view

urlpatterns = [
    path("pay/<int:borrowing_id>/", PayView.as_view(), name="pay"),
    path("config/", stripe_config),
    path(
        "create-checkout-session/<int:borrowing_id>/",
        create_checkout_session,
        name="create-checkout-session"
    ),
    path("success/<str:session_id>", success_view, name="success"),
]

app_name = "stripe_pay"
