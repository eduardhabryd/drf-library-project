from django.urls import path

from stripe_pay.views import PayView, stripe_config, create_checkout_session, success_view, cancelled_view, PayFineView, create_checkout_session_fine

urlpatterns = [
    path("pay/<int:borrowing_id>/", PayView.as_view(), name="pay"),
    path("pay-fine/<int:borrowing_id>/", PayFineView.as_view(), name="pay-fine"),
    path("config/", stripe_config),
    path(
        "create-checkout-session/<int:borrowing_id>/",
        create_checkout_session,
        name="create-checkout-session"
    ),
    path(
        "create-checkout-session-fine/<int:borrowing_id>/",
        create_checkout_session_fine,
        name="create-checkout-session-fine"
    ),
    path("success/", success_view, name="success"),
    path("cancel/", cancelled_view, name="cancel"),
    
]

app_name = "stripe_pay"
