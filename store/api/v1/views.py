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
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = models.Product.objects.select_related('base_product__category') \
            .prefetch_related(Prefetch(
                'base_product__properties',
                queryset=models.SetProductProperty.objects.select_related('property')
        )).all()

        if self.action == 'list':
            return queryset.defer(
                'inventory', 'unit', 'size','length_package', 'width_package', 'height_package',
                'weight_package', 'shenaase_kaala', 'barcode', 'product_status', 'active_status',
                'reason', 'base_product__title_english', 'base_product__product_code',
                'base_product__authenticity', 'base_product__warranty','base_product__shiping_method',
                'base_product__category__image', 'base_product__category__slug'
            )
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer
    
    def get_serializer_context(self):
        return {
            'images': models.ProductImage.objects.all()
        }
