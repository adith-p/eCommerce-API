from django.contrib import admin
from .models import Product_model, Product_image

# Register your models here.

admin.site.register(Product_model)
admin.site.register(Product_image)
