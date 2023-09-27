from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


import stripe
import os
import binascii

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentTestView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        "price": "price_1NsjS4IcB7Zsil8MHUmB1KJC",
                        "quantity": 1,
                    },
                ],
                # payment_method_types=["card"],
                mode="payment",
                success_url="http://localhost:8000/?success=true&session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:8000/?cancel=true&session_id={CHECKOUT_SESSION_ID}",
            )
        except Exception as e:
            return Response({"message": str(e)})
        return redirect(checkout_session.url)


class PaymentView(APIView):
    def post(self, request):
        # retrive the data from request.data and send in serilizer

        # continue if serializer.is_valid()
        try:
            __secret_key_for_user = os.urandom(32)
            secret_key_for_user = binascii.hexlify(__secret_key_for_user).decode()
            # store payemnt info in database
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": 2000,
                            "product_data": {
                                "name": "Test Product",
                            },
                        },
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url="http://localhost:8000/?success=true&session_id={CHECKOUT_SESSION_ID}&uid="
                + secret_key_for_user,
                cancel_url="http://localhost:8000/?cancel=true",
            )
            if checkout_session:
                # request.data["unique_id"] = checkout_session.id
                try:
                    amount = request.data["payment_name"]
                    unique_id = request.data["unique_id"]

                except:
                    amount = 0
                    unique_id = "0"
                check_id = checkout_session.id
                print("amount", amount)
                print("unique_id", unique_id)
                print("check_id", check_id)
                # update the payment info in database
                return redirect(checkout_session.url, status=201)
        except Exception as e:
            print("exception", e)
            return Response({"message": str(e)}, status=400)


# after payment is success validate the payment
