from rest_framework import serializers
from orders.models import Orders


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ('order_item', 'address', 'MOP')


class UpdateOrderSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=[
            ('cancel', 'Cancel'),
        ],
        required=True,
    )

    class Meta:
        model = Orders
        fields = ('status',)
