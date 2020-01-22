from __future__ import unicode_literals

from rest_framework import viewsets

from apps.catalogue import serializers as catalogue_serializers
from apps.catalogue.models import Category, Product, RequestedItem


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    serializer_class = catalogue_serializers.CategorySerializer
    queryset = Category.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    serializer_class = catalogue_serializers.ProductSerializer
    queryset = Product.objects.all()


class RequestedItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for requesting product instances.
    """
    serializer_class = catalogue_serializers.RequestedItemSerializer
    queryset = RequestedItem.objects.all()
