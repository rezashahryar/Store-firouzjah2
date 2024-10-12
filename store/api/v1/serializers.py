from rest_framework import serializers

from store import models

# create your serializers here


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']


class BaseProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    class Meta:
        model = models.BaseProduct
        fields = [
            'title_farsi', 'title_english', 'product_code', 'images'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    base_product = BaseProductDetailSerializer()
    
    class Meta:
        model = models.Product
        fields = [
            'base_product', 'size', 'inventory', 'unit', 'unit_price', 'discount_percent',
            'start_discount_datetime', 'end_discount_datetime'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')
    category = serializers.CharField(source='base_product.category')

    class Meta:
        model = models.Product
        fields = [
            'title', 'category', 'slug', 'unit_price', 'discount_percent', 'start_discount_datetime',
            'end_discount_datetime'
        ]
