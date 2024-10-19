from django_filters.rest_framework import FilterSet

from store.models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'base_product__category_id': ['exact'],
            'color_id': ['exact'],
            'unit_price': ['lte', 'gte']
        }
