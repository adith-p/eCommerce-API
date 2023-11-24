import environ
import razorpay

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from orders import models as omd
from .serializer import RazorPayStartPaymentSerializer, RazorPayFinishPaymentSerializer


env = environ.Env()
environ.Env.read_env()


class RazorpayStartPayment(APIView):
    """
    Class representing an API view for starting a payment with Razorpay.

    Methods:
        - post: Start a payment with Razorpay.

    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Start a payment with Razorpay.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with the payment details and the serialized data of the order if the data is valid,
            or a Response object with the validation errors if the data is invalid.

        """
        serializer = RazorPayStartPaymentSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data['order_item'])
            client = razorpay.Client(
                auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
            payment = client.order.create({"amount": int(serializer.validated_data['order_price']) * 100,
                                           "currency": "INR",
                                           "payment_capture": "1"})

            order_instance = omd.Orders.objects.get(
                pk=serializer.validated_data['order_item'])

            order_instance.order_payment_id = payment['id']
            order_instance.save()

            data = {
                "payment": payment,
                "order": serializer.data
            }
            return Response(data)
        return Response(serializer.errors)


class RazorpayPaymentSuccess(APIView):
    """
    Class representing an API view for handling successful payments with Razorpay.

    Methods:
        - post: Handle a successful payment with Razorpay.

    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle a successful payment with Razorpay.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with a success message if the payment is successfully verified and processed,
            or a Response object with the validation errors if the data is invalid,
            or a Response object with an error message if something goes wrong during payment processing.

        """
        serializer = RazorPayFinishPaymentSerializer(data=request.data)

        if serializer.is_valid():
            order_payment_id = serializer.validated_data['razorpay_order_id']
            order = omd.Orders.objects.get(order_payment_id=order_payment_id)

            client = razorpay.Client(
                auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

            check = client.utility.verify_payment_signature(serializer)

            if check is not None:
                print("Redirect to error url or error page")
                return Response({'error': 'Something went wrong'})

            order.status = 'ordered'
            order.save()

            res_data = {
                'message': 'payment successfully received!'
            }

            return Response(res_data, status=status.HTTP_200_OK)
        return Response(serializer.errors)
