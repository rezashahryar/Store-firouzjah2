import django_filters

from store.models import Product


class ListProductFilter(django_filters.FilterSet):
    custom_filter = django_filters.CharFilter(method='filter_by_color', label='color')
    available_products = django_filters.BooleanFilter(method='filter_available_products', label='available')

    class Meta:
        model = Product
        fields = {
            'unit_price': ['lte', 'gte'],
            'base_product__category': ['exact'],
            'base_product__brand': ['exact'],
        }

    def filter_by_color(self, queryset, name, value):
        return queryset.filter(items__item__name='رنگ', items__value=value)
    
    def filter_available_products(self, queryset, name, value):
        return Product.approved.available_products()
