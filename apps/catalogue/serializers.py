from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.catalogue.models import Category, Product, ProductStock, RequestedItem

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class ProductStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductStock
        fields = ('qty', 'limit')

    def validate(self, data):
        """
        Check that the stock quantity must be greater than stock limit.
        """
        if data['limit'] > data['qty']:
            raise serializers.ValidationError("Stock quantity should not be less than stock limit")
        return data


class ProductSerializer(serializers.ModelSerializer):

    stock = ProductStockSerializer()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'category', 'category_name', 'image', 'description', 'stock')

    def create(self, validated_data):
        kwargs = validated_data.pop('stock')
        instance = super().create(validated_data)
        ProductStock.objects.create(product=instance, **kwargs)
        return instance

    def update(self, instance, validated_data):
        kwargs = validated_data.pop('stock')
        instance = super().update(instance, validated_data)
        ProductStock.objects.filter(product=instance).update(**kwargs)
        return instance


class RequestedItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='product.name', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    timestamp = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = RequestedItem
        fields = ('product', 'product_name', 'qty', 'summary', 'user', 'status', 'timestamp')

    def get_status(self, obj):
        return obj.get_status_display()

    def validate(self, data):
        """
        Check the stock quantity before item requested.
        """
        requested_qty = data['qty']
        stock_qty = data['product'].stock.qty
        if not stock_qty:
            raise serializers.ValidationError("Stock is Empty. Request Later")
        if requested_qty > stock_qty:
            raise serializers.ValidationError("Stock contain only {} item left".format(stock_qty))
        return data

    def create(self, validated_data):
        validated_data['user'] = User.objects.first()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = User.objects.first()
        return super().update(instance, validated_data)
