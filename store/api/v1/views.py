from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from store import models

from . import serializers

# create your views here


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = models.Product.objects.select_related('base_product').all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer
