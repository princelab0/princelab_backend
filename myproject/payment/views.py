from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema

from payment.serializers import PaymentSerializer
from payment.models import Payment
from account.models import User


import stripe
import os
import binascii

# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        query_serializer=PaymentSerializer,
        responses={200: "User successfully created"},
    )
    def post(self, request, *args, **kwargs):
        # retrive the data from request.data and send in serilizer
        # request.data["user"] = request.user.id

        user_id = int(request.data["user"])
        user_instance = get_object_or_404(User, id=user_id)

        seriliazer = PaymentSerializer(data=request.data)
        print("seriliazer data ", seriliazer)
        print("seriliazer error")
        seriliazer.is_valid(raise_exception=True)
        print("seriliazer data", seriliazer.data)
        print("error1")
        try:
            __secret_key_for_user = os.urandom(32)
            secret_key_for_user = binascii.hexlify(__secret_key_for_user).decode()
            # store payemnt info in database
            print("error2")
            print(request.data["user"])
            uui_data = Payment.objects.create(
                user=user_instance,
                unique_id_for_user=secret_key_for_user,
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
                print("error4")
                # request.data["unique_id"] = checkout_session.id
                print("error5")
                # update the payment info in database
                Payment.objects.filter(
                    unique_id_for_user=uui_data.unique_id_for_user
                ).update(
                    user=user_instance,
                    payment_name=request.data["payment_name"],
                    payment_amount=request.data["payment_amount"],
                    unique_payment_id=checkout_session.id,
                )
                return Response(
                    {
                        "message": {
                            "checkoutSessionUrl": checkout_session.url,
                            "id": checkout_session.id,
                        }
                    },
                    status=201,
                )
                # return redirect(checkout_session.url)
            return Response({"message": "something went wrong"}, status=400)
        except Exception as e:
            print("exception", e)
            return Response({"message": str(e)}, status=400)


# after payment is success validate the payment
