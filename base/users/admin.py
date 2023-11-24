from django.contrib import admin
from .models import Users, Address, ShoppingCart, Wishlist

# Register your models here.
admin.site.register(Users)
# admin.site.register(Orders)
admin.site.register(Address)
admin.site.register(ShoppingCart)
admin.site.register(Wishlist)
