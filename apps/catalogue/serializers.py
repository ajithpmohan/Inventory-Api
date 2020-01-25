from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from apps.catalogue import fields
from apps.catalogue import models as catalogue_models

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = catalogue_models.Category
        fields = ('name',)


class ProductStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = catalogue_models.ProductStock
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
        model = catalogue_models.Product
        fields = ('name', 'category', 'category_name', 'image', 'description', 'stock')

    def create(self, validated_data):
        kwargs = validated_data.pop('stock')
        instance = super().create(validated_data)
        catalogue_models.ProductStock.objects.create(product=instance, **kwargs)
        return instance

    def update(self, instance, validated_data):
        kwargs = validated_data.pop('stock')
        instance = super().update(instance, validated_data)
        catalogue_models.ProductStock.objects.filter(product=instance).update(**kwargs)
        return instance


class RequestItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='product.name', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    timestamp = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = catalogue_models.RequestItem
        fields = ('product', 'product_name', 'qty', 'summary', 'user', 'status', 'timestamp')

    def get_status(self, obj):
        return obj.get_status_display()

    def validate(self, data):
        """
        Check the stock quantity before item requested.
        """
        requested_qty = data['qty']
        product = data['product']
        stock_qty = product.stock.qty
        if not stock_qty:
            raise serializers.ValidationError("{} stock is empty. Request Later".format(product))
        if requested_qty > stock_qty:
            raise serializers.ValidationError("{} item contain only {} stock left".format(product, stock_qty))
        return data

    def create(self, validated_data):
        validated_data['user'] = User.objects.first()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = User.objects.first()
        return super().update(instance, validated_data)


class IssueItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source='product.name', read_only=True)
    requested_item = serializers.HiddenField(default=fields.CurrentRequestItemDefault())
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # WIP
    username = serializers.CharField(source='user.username', read_only=True)
    timestamp = serializers.DateTimeField(format='%d/%m/%Y %H:%M', read_only=True)

    class Meta:
        model = catalogue_models.IssueItem
        fields = ('product_name', 'requested_item', 'username', 'qty', 'summary', 'timestamp')

    def validate(self, data):
        """
        Check the stock quantity before item requested.
        """
        requested_item = data['requested_item']
        product = getattr(requested_item, 'product')

        product_stock_qty = product.stock.qty
        issue_stock_qty = data['qty']

        # Check if item is already issued
        if hasattr(requested_item, 'issueitems'):
            raise serializers.ValidationError("{} is already issued".format(product))

        # Check the product stock quantity
        if not product_stock_qty:
            raise serializers.ValidationError("{} stock is empty. Refill it".format(product))

        # Item can't be issued when issue stock quantity greater than product stock qty
        if issue_stock_qty > product_stock_qty:
            raise serializers.ValidationError("{} item contain only {} stock left".format(product, product_stock_qty))

        # Item can't be issued when issue stock quantity greater than user requested stock qty
        if issue_stock_qty > requested_item.qty:
            raise serializers.ValidationError("Requested Stock is {} quantity".format(requested_item.qty))
        return data

    def create(self, validated_data):
        validated_data['user'] = User.objects.first()
        validated_data['product'] = getattr(validated_data['requested_item'], 'product')

        with transaction.atomic():
            instance = super().create(validated_data)
            # Product stock get reduced after issuing
            product_stock = validated_data['product'].stock
            product_stock.qty = product_stock.qty-validated_data['qty']
            product_stock.save()
            # update requested item status after issuing
            validated_data['requested_item'].status = catalogue_models.RequestItem.APPROVED
            validated_data['requested_item'].save()
            return instance
