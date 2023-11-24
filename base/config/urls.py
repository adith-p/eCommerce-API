from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version='v1',
        description="An Ecommerce API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="adithprakash008@gmail.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include('product.api.urls')),
    path('auth/', include('auth.api.urls')),
    path('user/', include('users.api.urls')),
    path('order/', include('orders.api.urls')),
    path('razorpay/', include('razorpay_backend.api.urls')),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),


]
