from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer


# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Add serializer_class

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                "error": "Serializer not found, Create Product first."
            }, status=status.HTTP_404_NOT_FOUND)

        queryset_serializer = ProductSerializer(queryset, many=True)
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