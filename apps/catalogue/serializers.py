from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.catalogue.models import Category, Product, ProductStock

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

    class Meta:
        model = Product
        fields = ('name', 'category', 'image', 'description', 'stock')

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
