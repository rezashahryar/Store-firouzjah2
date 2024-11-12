from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from store import models

from . import serializers
from .paginations import ListProductPagination


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = models.Product.objects.select_related('base_product__category').all()
    serializer_class = serializers.ListProductSerializer
    pagination_class = ListProductPagination

    def get_serializer_context(self):
        return {'images': models.ProductImage.objects.all()}
