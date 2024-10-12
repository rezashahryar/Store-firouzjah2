from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins

from store import models

from . import serializers

# create your views here


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = models.Product.objects.select_related('base_product').all()
    serializer_class = serializers.ProductDetailSerializer
