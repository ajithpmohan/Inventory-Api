from __future__ import unicode_literals

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.catalogue import models as catalogue_models
from apps.catalogue import serializers as catalogue_serializers


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.
    """
    serializer_class = catalogue_serializers.CategorySerializer
    queryset = catalogue_models.Category.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    serializer_class = catalogue_serializers.ProductSerializer
    queryset = catalogue_models.Product.objects.all()


class RequestItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for requesting product instances.
    """
    # serializer_class = catalogue_serializers.RequestItemSerializer
    queryset = catalogue_models.RequestItem.objects.all()

    def get_serializer_class(self):
        if self.action == 'issueitem':
            return catalogue_serializers.IssueItemSerializer
        else:
            return catalogue_serializers.RequestItemSerializer

    def get_serializer_context(self):
        kwargs = super().get_serializer_context()
        if self.action == 'issueitem':
            kwargs['requested_item'] = self.get_object()
        return kwargs

    @action(detail=True, methods=['get', 'post'])
    def issueitem(self, request, pk=None):
        if request.POST:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                # check product stock qty and send stock limit notification to admin when it is below the limit level
                self.get_object().product.stock_limit_notif(request)

                requested_item = catalogue_serializers.RequestItemSerializer(self.get_object()).data
                return Response(
                    {'Requested Item': requested_item, 'Related Issued Item': serializer.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        requested_item = catalogue_serializers.RequestItemSerializer(self.get_object()).data

        # Check if item is already issued
        if hasattr(self.get_object(), 'issueitems'):
            related_issued_item = catalogue_serializers.IssueItemSerializer(self.get_object().issueitems).data
            return Response({'Requested Item': requested_item, 'Related Issued Item': related_issued_item})
        return Response({'Requested Item': requested_item})
