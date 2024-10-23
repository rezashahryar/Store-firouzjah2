from rest_framework import serializers

from panel import models
from store import models as store_models

# create your serializers here


class OrderItemSerializer(serializers.ModelSerializer):
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = store_models.OrderItem
        fields = ['product_code']

    def get_product_code(self, order_item):
        return order_item.product.base_product.product_code


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = store_models.Order
        fields = ['tracking_code', 'items']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['full_name', 'mobile', 'email']


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ['id', 'title', 'text']


class CommonQuestionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    main_subject = serializers.CharField(source='get_main_subject_display')
    
    class Meta:
        model = models.CommonQuestion
        fields = ['type', 'main_subject', 'title', 'text']


class FeeForSellingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeeForSellingProduct
        fields = ['category', 'sub_category', 'product_type', 'fee_percent']
