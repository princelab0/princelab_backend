from django.urls import path

from payment import views

urlpatterns = [
    path("stripe_payment/", views.PaymentView.as_view(), name="payment"),
]
