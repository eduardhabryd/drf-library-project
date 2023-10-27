from django.urls import path

from stripe_pay.views import PayView, stripe_config, create_checkout_session, success_view, cancelled_view

urlpatterns = [
    path("pay/<int:borrowing_id>/", PayView.as_view(), name="pay"),
    path("config/", stripe_config),
    path(
        "create-checkout-session/<int:borrowing_id>/",
        create_checkout_session,
        name="create-checkout-session"
    ),
    path("success/", success_view, name="success"),
    path("cancel/", cancelled_view, name="cancel"),
    
]

app_name = "stripe_pay"
