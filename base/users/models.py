from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from product import models as md
# from model import shoppingkart
# Create your models here.
indian_cities = (
    ('KOCH', 'Kochi'),
    ('BLR', 'Bangalore'),
    ('CHN', 'Chennai'),
    ('HYD', 'Hyderabad'),
    ('AMD', 'Ahmedabad'),
    ('KOL', 'Kolkata'),
    ('SUR', 'Surat'),
    ('PUN', 'Pune'),
    ('JAI', 'Jaipur'),
    ('LKO', 'Lucknow'),
    ('KAN', 'Kanpur'),
    ('NAG', 'Nagpur'),
    ('IND', 'Indore'),
    ('THA', 'Thane'),
    ('PCM', 'Pimpri-Chinchwad'),
    ('AMDC', 'Ahmedabad City'),
    ('VAD', 'Vadodara'),
    ('GZB', 'Ghaziabad'),
    ('LUD', 'Ludhiana'),
    ('AGR', 'Agra'),
    ('SMC', 'Surat Municipal Corporation'),
    ('MER', 'Meerut'),
)

state_tuples = (
    ('Andhra Pradesh', 'AP'),
    ('Arunachal Pradesh', 'AR'),
    ('Assam', 'AS'),
    ('Bihar', 'BR'),
    ('Chhattisgarh', 'CG'),
    ('Goa', 'GA'),
    ('Gujarat', 'GJ'),
    ('Haryana', 'HR'),
    ('Himachal Pradesh', 'HP'),
    ('Jharkhand', 'JH'),
    ('Karnataka', 'KA'),
    ('Kerala', 'KL'),
    ('Madhya Pradesh', 'MP'),
    ('Maharashtra', 'MH'),
    ('Manipur', 'MN'),
    ('Meghalaya', 'ML'),
    ('Mizoram', 'MZ'),
    ('Nagaland', 'NL'),
    ('Odisha', 'OD'),
    ('Punjab', 'PB'),
    ('Rajasthan', 'RJ'),
    ('Sikkim', 'SK'),
    ('Tamil Nadu', 'TN'),
    ('Telangana', 'TS'),
    ('Tripura', 'TR'),
    ('Uttar Pradesh', 'UP'),
    ('Uttarakhand', 'UK'),
    ('West Bengal', 'WB'),
    ('Andaman and Nicobar Islands', 'AN'),
    ('Chandigarh', 'CH'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'DN'),
    ('Lakshadweep', 'LD'),
    ('Delhi', 'DL'),
    ('Puducherry', 'PY')
)


class Users(AbstractUser):
    pass


class Address(models.Model):
    adress_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    street = models.CharField(max_length=255, blank=False)
    city = models.CharField(choices=indian_cities, max_length=100)
    state = models.CharField(choices=state_tuples, max_length=100)
    zipcode = models.BigIntegerField()
    user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='address')


class ShoppingCart(models.Model):
    shopping_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    shopping_item = models.ManyToManyField(
        md.Product_model)
    user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='cart_user_id')


class Wishlist(models.Model):
    wishlist_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    whishlist_item = models.ManyToManyField(
        md.Product_model)
    user_id = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name='wish_user_id')
