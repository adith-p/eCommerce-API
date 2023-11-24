from django.urls import path
from .views import GetUserProfileView, RegisterUserProfileView, ShoppingcartApiView, WishlistApiView, AddressApiView, AddressUpdateView, WishlistUpdateView, ShoppingCartUpdateView

from orders.api.views import GetUpdateOrderApiView, OrderAPIView


urlpatterns = [
    path('', RegisterUserProfileView.as_view(), name='register_user'),
    path('me/', GetUserProfileView.as_view(), name='user_profile'),
    path('me/address/', AddressApiView.as_view(), name='user_address'),
    path('me/address/<address_id>/',
         AddressUpdateView.as_view(), name='user_address_id'),
    path('me/shoppingcart/', ShoppingcartApiView.as_view(), name='shopping_cart'),
    path('me/shoppingcart/<product_id>/',
         ShoppingCartUpdateView.as_view(), name='shopping_cart'),
    path('me/wishlist/', WishlistApiView.as_view(), name='wishlist'),
    path('me/wishlist/<product_id>/',
         WishlistUpdateView.as_view(), name='wishlist_id'),

    path('me/orders/', OrderAPIView.as_view(), name='wishlist'),
    path('me/orders/<order_id>/', GetUpdateOrderApiView.as_view(), name='wishlist'),
]
