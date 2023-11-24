from rest_framework import serializers
from users.models import Address, Users,  ShoppingCart, Wishlist
from product.api.serializer import W_S_ProductSerializer


class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user_id',]


class PasswordSerializers(serializers.ModelSerializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    class Meta:
        model = Users
        fields = ['new_password', 'old_password']


class DisplayUserSerializer(serializers.ModelSerializer):
    address = AddressSerializers(read_only=True, many=True)

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email', 'address',)


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email')


class WishlistSerializer(serializers.ModelSerializer):
    whishlist_item = W_S_ProductSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ['whishlist_item',]


class ShoppingcartSerializer(serializers.ModelSerializer):
    shopping_item = W_S_ProductSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['shopping_item',]
