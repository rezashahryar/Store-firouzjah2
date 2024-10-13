from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework import mixins
from django.db.models import Prefetch

from store import models

from . import serializers

# create your views here


class ProductCategoryListApiView(generics.ListAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = models.Product.objects.select_related('base_product').prefetch_related(Prefetch(
        'base_product__properties',
        queryset=models.SetProductProperty.objects.select_related('property')
    )).all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer
