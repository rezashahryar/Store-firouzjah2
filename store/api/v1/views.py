from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from panel.models import SetProductItem
from store import models

from . import serializers
from .paginations import ListProductPagination
from .filters import ListProductFilter


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['base_product__title_farsi']
    filterset_class = ListProductFilter
    ordering_fields = ['datetime_created', 'unit_price', 'count_sell']
    pagination_class = ListProductPagination
    # lookup_field = 'slug'

    def get_queryset(self):
        queryset = models.Product.approved.select_related('base_product__category') \
            .select_related('base_product__sub_category').all()
        if self.action == 'retrieve':
            return queryset.prefetch_related(Prefetch(
                'items',
                queryset=SetProductItem.objects.select_related('item')
            )).select_related('base_product__store').prefetch_related('base_product__images')
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        return serializers.ListProductSerializer

    def filter_queryset(self, queryset):
        ordering = self.request.GET.get("ordering", None)
        # ordering by property field
        if ordering is not None:
            if ordering == 'count_sell':
                queryset = queryset.annotate(count_selll=Count('order_items')).order_by('count_selll')
            if ordering == '-count_sell':
                queryset = queryset.annotate(count_selll=Count('order_items')).order_by('-count_selll')
            return queryset
        
        return super().filter_queryset(queryset)

    def get_serializer_context(self):
        return {'images': models.ProductImage.objects.all()}
    

class ProductCategoryListApiView(generics.ListAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer


class ProductBrandListApiView(generics.ListAPIView):
    queryset = models.ProductBrand.objects.all()
    serializer_class = serializers.ProductBrandSerializer
