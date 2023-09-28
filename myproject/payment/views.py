from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from payment.serializers import PaymentSerializer
from payment.models import Payment


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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # retrive the data from request.data and send in serilizer
        # request.data["user"] = request.user.id

        seriliazer = PaymentSerializer(data=request.data)
        print("seriliazer", seriliazer)
        print("error")
        seriliazer.is_valid(raise_exception=True)
        print("seriliazer data", seriliazer.data)
        print("error1")
        try:
            __secret_key_for_user = os.urandom(32)
            secret_key_for_user = binascii.hexlify(__secret_key_for_user).decode()
            # store payemnt info in database
            print("error2")
            print(request.user.id)
            uui_data = Payment.objects.create(
                user=request.user, unique_id_for_user=secret_key_for_user
            )
            print("error3")
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": int(request.data["payment_amount"]),
                            "product_data": {
                                "name": request.data["payment_name"],
                            },
                        },
                        "quantity": 1,
                    },
                ],
                metadata={"product_id": request.data["payment_name"]},
                payment_method_types=[
                    "card",
                ],
                mode="payment",
                success_url="http://localhost:8000/?success=true&session_id={CHECKOUT_SESSION_ID}&uid="
                + secret_key_for_user,
                cancel_url="http://localhost:8000/?cancel=true",
            )
            if checkout_session:
                request.data["unique_id"] = checkout_session.id
                # update the payment info in database
                Payment.objects.filter(
                    unique_id_for_user=uui_data.unique_id_for_user
                ).update(
                    user=request.user,
                    payment_name=request.data["payment_name"],
                    payment_amount=request.data["payment_amount"],
                    unique_payment_id=checkout_session.id,
                    payment_status=True,
                )
                return redirect(checkout_session.url, status=201)
        except Exception as e:
            print("exception", e)
            return Response({"message": str(e)}, status=400)


# after payment is success validate the payment
