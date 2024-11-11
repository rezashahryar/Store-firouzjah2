import django_filters

from store import models as store_models


class OrderFilter(django_filters.FilterSet):
    # product_code = django_filters.CharFilter(
    #     field_name='items__product__product_code',
    #     lookup_expr='contains',
    #     label='product_code',
    # )
    store_code = django_filters.CharFilter(
        field_name='items__product__base_product__store__store_code',
        lookup_expr='contains',
        label='store_code'
    )
    store_mobile = django_filters.CharFilter(
        field_name='items__product__base_product__store__mobile_num',
        lookup_expr='contains',
        label='store_mobile'
    )
    user_email = django_filters.CharFilter(
        field_name='user__email',
        lookup_expr='icontains',
        label='email_of_user'
    )

    class Meta:
        model = store_models.Order
        fields = {
            'tracking_code': ['contains'],
            'status': ['exact']
        }
