from rest_framework import serializers
from product.models import Product_model, Product_image


class ProductImageSerialilzer(serializers.ModelSerializer):
    class Meta:
        model = Product_image
        fields = ('pr_img',)


class ProductSerializer(serializers.ModelSerializer):
    product = ProductImageSerialilzer(read_only=True, many=True)

    class Meta:
        model = Product_model
        fields = ('product_id', 'product_name',
                  'pr_desc', 'pr_price', 'product')


class W_S_ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product_model
        fields = ('product_id', 'product_name',)


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_model
        fields = ('product_name', 'pr_desc', 'pr_price',)


class UpdateProductSerailizer(serializers.ModelSerializer):

    class Meta:
        model = Product_model
        fields = ('product_name', 'pr_desc', 'pr_price',)
