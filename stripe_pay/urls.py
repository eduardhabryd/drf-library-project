from django.urls import path

from stripe_pay.views import PayView, stripe_config, create_checkout_session

urlpatterns = [
    path("pay/", PayView.as_view(), name="home"),
    path("config/", stripe_config),
    path("create-checkout-session/", create_checkout_session),
]
