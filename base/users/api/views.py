
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .serializer import DisplayUserSerializer, RegisterUserSerializer, UpdateUserSerializer, ShoppingcartSerializer, WishlistSerializer, PasswordSerializers, AddressSerializers

from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema


from users.models import Users, ShoppingCart, Address
from product.models import Product_model


class GetUserProfileView(APIView):

    """
    Class representing an API view for retrieving, updating, and deleting a user profile.

    Methods:
        - get_user_instance: Get the user instance of the authenticated user.
        - get: Retrieve the user profile.
        - delete: Delete the user profile.
        - put: Update the user profile.
        - patch: Change the user password.
    """
    permission_classes = [IsAuthenticated]

    def get_user_instance(self):
        return Users.objects.get(pk=self.request.user.pk)

    def get(self, request):
        """
        Retrieve the user profile.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object containing the serialized data of the user profile.

        """
        user_instance = self.get_user_instance()
        serializer = DisplayUserSerializer(user_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Delete the user profile.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with a success status if the user profile is deleted successfully.

        """
        user_instance = self.get_user_instance()
        user_instance.delete()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UpdateUserSerializer,
        responses={200: UpdateUserSerializer}

    )
    def put(self, request):
        """
        Update the user profile.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with the serialized data of the updated user profile if the data is valid,
            or a Response object with the validation errors if the data is invalid.

        """

        user_instance = self.get_user_instance()
        serializer = UpdateUserSerializer(user_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=PasswordSerializers,

    )
    def patch(self, request):
        """
        Change the user password.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with a success status if the password is changed successfully,
            or a Response object with an unauthorized status if the old password is incorrect,
            or a Response object with the validation errors if the data is invalid.

        """
        user_instance = self.get_user_instance()
        serializer = PasswordSerializers(data=request.data)
        if serializer.is_valid():
            if not user_instance.check_password(
                    serializer.validated_data['old_password']):
                return Response(status=status.HTTP_401_UNAUTHORIZED, data={'r': 'wrong password'})
            user_instance.set_password(
                serializer.validated_data['new_password'])
            user_instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)


class RegisterUserProfileView(APIView):

    """
    Class representing an API view for registering a user profile.

    Methods:
        - get_permissions: Get the permissions required for different HTTP methods.
        - post: Register a new user profile.
    """
    permission_classes = [AllowAny]

    def get_permissions(self):
        return [AllowAny()] if self.request.method in ['POST'] else [IsAuthenticated()]

    @swagger_auto_schema(
        responses={200: RegisterUserSerializer},

    )
    def post(self, request):
        """
        Register a new user profile.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with the serialized data of the registered user profile if the data is valid,
            or a Response object with the validation errors if the data is invalid.

        """

        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            user_instance = Users.objects.create(
                username=username, email=email)
            user_instance.set_password(password)
            user_instance.save()
            shoppingcart = ShoppingCart.objects.create(user_id=user_instance)
            shoppingcart.save()

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShoppingcartApiView(APIView):
    """
    Class representing an API view for managing a user's shopping cart.

    Methods:
        - get_queryset: Get the shopping cart queryset for a specific user.
        - get: Retrieve the shopping cart items for the authenticated user.
        - patch: Remove a specific product from the shopping cart.
        - put: Add a specific product to the shopping cart.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, id):  # sourcery skip: assign-if-exp, reintroduce-else
        u1 = Users.objects.get(pk=id)
        shopping_instance = u1.cart_user_id.all()

        print(shopping_instance)
        if shopping_instance:
            return shopping_instance

    @swagger_auto_schema(
        responses={200: ShoppingcartSerializer},
        tags=['Shopping Cart'],
    )
    def get(self, request):
        """
        Retrieve the shopping cart items for the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object containing the serialized data of the shopping cart items.

        """
        shopping_instance = self.get_queryset(request.user.id)
        print(shopping_instance)
        serializer = ShoppingcartSerializer(
            shopping_instance, many=True)
        return Response(serializer.data)


class ShoppingCartUpdateView(APIView):
    # sourcery skip: assign-if-exp, reintroduce-else, use-named-expression
    permission_classes = [IsAuthenticated]

    def get_queryset(self, id):

        u1 = Users.objects.get(pk=id)
        shopping_instance = u1.cart_user_id.all()

        if shopping_instance:
            return shopping_instance

    @swagger_auto_schema(
        responses={200: '200_ok', 404: 'product does not exist'},
        tags=['Shopping Cart'],
    )
    def patch(self, request, product_id):
        """
        Remove a specific product from the shopping cart.

        Args:
            request: The HTTP request object.
            product_id: The ID of the product to be removed from the shopping cart.

        Returns:
            A Response object with a success status if the product is removed successfully.

        """

        shopping_instance = self.get_queryset(request.user.id)
        product_instance = get_object_or_404(Product_model, pk=product_id)
        shopping_instance[0].shopping_item.remove(product_instance)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: '200_ok', 404: 'product does not exist'},
        tags=['Shopping Cart'],
    )
    def put(self, request, product_id):
        """
        Add a specific product to the shopping cart.

        Args:
            request: The HTTP request object.
            product_id: The ID of the product to be added to the shopping cart.

        Returns:
            A Response object with a success status if the product is added successfully.

        """
        shopping_instance = self.get_queryset(request.user.id)
        product_instance = get_object_or_404(Product_model, pk=product_id)
        shopping_instance[0].shopping_item.add(product_instance)
        return Response(status=status.HTTP_200_OK, data={'r': '200_OK'})


class WishlistApiView(APIView):
    """
    Class representing an API view for managing a user's wishlist.

    Methods:
        - get_queryset: Get the wishlist queryset for a specific user.
        - get: Retrieve the wishlist items for the authenticated user.
        - patch: Remove a specific product from the wishlist.
        - put: Add a specific product to the wishlist.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self, id):  # sourcery skip: assign-if-exp, reintroduce-else
        u1 = Users.objects.get(pk=id)
        if wishlist_instance := u1.wish_user_id.all():
            return wishlist_instance

    @swagger_auto_schema(
        responses={200: '200_ok', 404: 'product does not exist'},
        tags=['Wishlist'],
    )
    def get(self, request):
        """
        Retrieve the wishlist items for the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object containing the serialized data of the wishlist items.

        """
        wishlist_instance = self.get_queryset(request.user.id)
        serializer = WishlistSerializer(
            wishlist_instance, many=True)
        return Response(serializer.data)


class WishlistUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, id):  # sourcery skip: assign-if-exp, reintroduce-else
        u1 = Users.objects.get(pk=id)
        if wishlist_instance := u1.wish_user_id.all():
            return wishlist_instance

    @swagger_auto_schema(
        responses={204: 'NO_CONTENT', 404: 'product does not exist'},
        tags=['Wishlist'],
    )
    def patch(self, request, product_id):
        """
        Remove a specific product from the wishlist.

        Args:
            request: The HTTP request object.
            product_id: The ID of the product to be removed from the wishlist.

        Returns:
            A Response object with a success status if the product is removed successfully.

        """
        wishlist_instance = self.get_queryset(request.user.id)
        product_instance = get_object_or_404(Product_model, pk=product_id)
        wishlist_instance[0].whishlist_item.remove(product_instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={200: '200_ok', 404: 'product does not exist'},
        tags=['Wishlist'],

    )
    def put(self, request, product_id):
        """
        Add a specific product to the wishlist.

        Args:
            request: The HTTP request object.
            product_id: The ID of the product to be added to the wishlist.

        Returns:
            A Response object with a success status if the product is added successfully.

        """
        wishlist_instance = self.get_queryset(request.user.id)
        product_instance = get_object_or_404(Product_model, pk=product_id)
        wishlist_instance[0].whishlist_item.add(product_instance)
        return Response(status=status.HTTP_200_OK, data={'r': '200_OK'})


class AddressApiView(APIView):
    """
    Class representing an API view for creating and retrieving user addresses.

    Methods:
        - get_user_instance: Get the user instance of the authenticated user.
        - get: Retrieve the addresses associated with the authenticated user.
        - post: Create a new address for the authenticated user.

    """

    permission_classes = [IsAuthenticated]

    def get_user_instance(self):
        return Users.objects.get(pk=self.request.user.id)

    @swagger_auto_schema(
        responses={200: AddressSerializers},
        tags=['address'],

    )
    def get(self, request):
        """
        Retrieve the addresses associated with the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object containing the serialized data of the addresses.

        """
        usr_instance = self.get_user_instance()
        address_instance = usr_instance.address.all()
        serializer = AddressSerializers(address_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AddressSerializers,
        responses={200: AddressSerializers, 400: 'validation_error'},
        tags=['address']
    )
    def post(self, request):
        """
        Create a new address for the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with a success message if the address is created successfully,
            or a Response object with the validation errors if the data is invalid.

        """
        usr_instance = self.get_user_instance()
        serializer = AddressSerializers(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user_id'] = usr_instance
            serializer.save()
            return Response({'message': 'done'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressUpdateView(APIView):
    """
    Class representing an API view for updating and deleting user addresses.

    Methods:
        - delete: Delete a specific address.
        - put: Update a specific address.

    """
    @swagger_auto_schema(
        request_body=AddressSerializers,
        responses={200: 'done', 400: 'validation_error'},
        tags=['address']

    )
    def patch(self, request, address_id):
        """
        Update a specific address.

        Args:
            request: The HTTP request object.
            address_id: The ID of the address to be updated.

        Returns:
            A Response object with a success message if the address is updated successfully,
            or a Response object with the validation errors if the data is invalid.

        """
        address_instance = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializers(
            address_instance, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'message': 'done'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['address'],
        responses={204: 'NO_CONTENT'}
    )
    def delete(self, request, address_id):
        """
        Delete a specific address.

        Args:
            request: The HTTP request object.
            address_id: The ID of the address to be deleted.

        Returns:
            A Response object with a success status if the address is deleted successfully.

        """
        address_instance = get_object_or_404(Address, pk=address_id)
        address_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
