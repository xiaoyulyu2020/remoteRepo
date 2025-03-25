from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, User
from products.rabbitmq import send_to_queue, publish
from products.serializers import ProductSerializer, UserSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Add serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)

        queryset_serializer = self.get_serializer(queryset, many=True)
        publish()
        return Response(queryset_serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({"message": "Delete successfully"},status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        # Prepare product data for RabbitMQ
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }

        # Try to send message to RabbitMQ
        try:
            send_to_queue(product_data)
        except Exception as e:
            # Log the error (make sure you have logging configured)
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send product data to RabbitMQ: {str(e)}")

            # You may choose to return a warning message or proceed
            return Response(
                {"message": "Product created, but failed to notify RabbitMQ"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs) -> Response:
        users = self.get_queryset()
        if not users.exists():
            return Response([], status=status.HTTP_200_OK)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs) -> Response:
        user = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs) -> Response:
        user = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs) -> Response:
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"message": "Delete successfully"},status=status.HTTP_204_NO_CONTENT)