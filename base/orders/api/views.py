from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema

from orders.models import Orders
from .serializers import OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
from users.models import Users


class OrderAPIView(APIView):
    """
    Class representing an API view for orders.

    Methods:
        - get: Retrieve all orders.
        - post: Create a new order.
        - patch: Update an existing order.
    """

    def get_user_instance(self):
        return Users.objects.get(pk=self.request.user.id)

    @swagger_auto_schema(
        responses={200: OrderSerializer},
        tags=['Orders']

    )
    def get(self, request):
        """
        Retrieve all orders.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object containing the serialized data of all orders.

        """
        user_instance = self.get_user_instance()

        order_instance = user_instance.order_user_id.all()
        serializer = OrderSerializer(order_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrderApiView(APIView):

    @swagger_auto_schema(
        request_body=CreateOrderSerializer,
        responses={200: 'order placed', 102: 'Order processed'},
        tags=['Create Order']
    )
    def post(self, request):
        """
        Create a new order.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with a success message if the order is placed successfully,
            or a Response object with a processing message if the order is placed with 'cod' payment method.

        """

        serializer = CreateOrderSerializer(data=request.data)
        try:
            user_instance = get_object_or_404(Users, pk=request.user.id)
        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.validated_data['user_id'] = user_instance
            if serializer.validated_data['MOP'] != 'cod':
                serializer.validated_data['status'] = 'processed'
                serializer.save()
                return Response({'message': 'Order Placed'}, status=status.HTTP_200_OK)
            serializer.save()
            return Response({'message': 'Order processed, waiting for payment confirmation'}, status=status.HTTP_102_PROCESSING)


class GetUpdateOrderApiView(APIView):
    @swagger_auto_schema(
        responses={200: OrderSerializer, 404: 'order does not exist'},
        tags=['Orders']
    )
    def get(self, request, order_id):
        """
        Retrieve an order.

        Args:
            request: The HTTP request object.
            order_id: The ID of the order to be retrieved.

        Returns:
            A Response object with the serialized data of the order if it exists,
            or a Response object with a 'order does not exist' message if the order is not found.

        """
        try:
            order_instance = get_object_or_404(Orders, pk=order_id)
        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UpdateOrderSerializer,
        tags=['Orders']

    )
    def patch(self, request, order_id):
        """
        Update an existing order.

        Args:
            request: The HTTP request object.
            order_id: The ID of the order to be updated.

        Returns:
            A Response object with a success message if the order is updated successfully,
            or a Response object with the validation errors if the update fails.

        """
        try:
            order_instance = get_object_or_404(Orders, pk=order_id)
        except Exception as e:
            return Response({'message': e}, status=status.HTTP_200_OK)
        serializer = UpdateOrderSerializer(
            order_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Updated successfully '}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
