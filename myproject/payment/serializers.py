from rest_framework import serializers
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    payment_name = serializers.ChoiceField(choices=["stripe"], required=True)

    class Meta:
        model = Payment
        fields = (
            "user",
            "payment_name",
            "payment_amount",
        )

    def validate_payment_amount(self, payment_amount):
        try:
            if payment_amount <= 0:
                raise serializers.ValidationError("Payment amount is not valid")
        except:
            raise serializers.ValidationError("Payment error exception")
        return payment_amount
