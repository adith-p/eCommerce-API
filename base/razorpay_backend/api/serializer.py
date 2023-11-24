from rest_framework import serializers


class RazorPayStartPaymentSerializer(serializers.Serializer):
    order_item = serializers.UUIDField()
    order_price = serializers.DecimalField(decimal_places=2, max_digits=7)


class RazorPayFinishPaymentSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()
