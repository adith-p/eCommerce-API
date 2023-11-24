
from django.urls import path
from .views import List_products, Get_product
urlpatterns = [
    path('product/', List_products.as_view(), name='list_products'),
    path('product/<id>/', Get_product.as_view(), name='get_products'),
]
