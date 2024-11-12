from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework import mixins
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from store import models

from . import serializers
from .paginations import ListProductPagination
from .filters import ListProductFilter


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = models.Product.approved.select_related('base_product__category').all()
    serializer_class = serializers.ListProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ListProductFilter
    ordering_fields = ['datetime_created', 'unit_price']
    pagination_class = ListProductPagination

    def get_serializer_context(self):
        return {'images': models.ProductImage.objects.all()}
    

class ProductCategoryListApiView(generics.ListAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer
