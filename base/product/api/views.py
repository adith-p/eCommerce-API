from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from product.models import Product_model
from .serializer import ProductSerializer, CreateProductSerializer, UpdateProductSerailizer, ProductImageSerialilzer


class List_products(APIView):
    """
    Class representing an API view for listing products.

    Methods:
        - get_permissions: Get the permissions required for different HTTP methods.
        - get: Retrieve all products.
        - post: Create a new product.
    """

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'POST']:
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        responses={200: ProductSerializer},

    )
    def get(self, request):
        """
        Retrieve all products.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object containing the serialized data of all products.

        """
        search_query = request.GET.get('search', '')
        if search_query:
            query_set = Product_model.objects.filter(
                Q(product_name__icontains=search_query) | Q(pr_desc__icontains=search_query))
        else:
            query_set = Product_model.objects.all()
        serializer = ProductSerializer(query_set, many=True)
        return Response(serializer.data)
        # query_set = Product_model.objects.all()
        # serializer = ProductSerializer(query_set, many=True)
        # return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CreateProductSerializer,
        responses={201: CreateProductSerializer}
    )
    def post(self, request):
        """
        Create a new product.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with the serialized data of the created product if the data is valid,
            or a Response object with the validation errors if the data is invalid.

        """
        serializer = CreateProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Get_product(APIView):
    """
    Class representing an API view for retrieving, updating, creating, and deleting a product.

    Methods:
        - get_permissions: Get the permissions required for different HTTP methods.
        - get: Retrieve a specific product.
        - put: Update a specific product.
        - post: Create an image for a specific product.
        - delete: Delete a specific product.
    """

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'POST']:
            return [IsAdminUser()]
        return [AllowAny()]

    @swagger_auto_schema(
        responses={200: ProductSerializer}
    )
    def get(self, request, id):
        """
        Retrieve a specific product.

        Args:
            request: The HTTP request object.
            id: The ID of the product to be retrieved.

        Returns:
            A Response object containing the serialized data of the specified product.

        """
        query_set = Product_model.objects.get(pk=id)
        serializer = ProductSerializer(query_set)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UpdateProductSerailizer,
        responses={200: UpdateProductSerailizer}
    )
    def put(self, request, id):
        """
        Update a specific product.

        Args:
            request: The HTTP request object.
            id: The ID of the product to be updated.

        Returns:
            A Response object with the serialized data of the updated product if the data is valid,
            or a Response object with the validation errors if the data is invalid.

        """
        product_instance = get_object_or_404(
            Product_model, pk=id)
        serializer = UpdateProductSerailizer(
            product_instance, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"r": serializer.data})

    @swagger_auto_schema(
        request_body=ProductImageSerialilzer,
        responses={200: ProductImageSerialilzer},
        tags=['Image']


    )
    def post(self, request, id):
        """
        Create an image for a specific product.

        Args:
            request: The HTTP request object.
            id: The ID of the product for which the image is being created.

        Returns:
            A Response object with the serialized data of the created image if the data is valid,
            or a Response object with the validation errors if the data is invalid.

        """
        serializer = ProductImageSerialilzer(data=request.data)
        product_instance = get_object_or_404(
            Product_model, pk=id)
        if serializer.is_valid():
            serializer.validated_data['prid'] = product_instance
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'No_content'}


    )
    def delete(self, request, id):
        """
        Delete a specific product.

        Args:
            request: The HTTP request object.
            id: The ID of the product to be deleted.

        Returns:
            A Response object with a success message if the product is deleted successfully.

        """
        product_instance = get_object_or_404(
            Product_model, pk=id)
        product_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchApiView(APIView):
    ...
