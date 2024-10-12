from rest_framework import serializers

from store import models

# create your serializers here


class BaseProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BaseProduct
        fields = [
            'title_farsi', 'title_english'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    base_product = BaseProductDetailSerializer()
    
    class Meta:
        model = models.Product
        fields = [
            'base_product'
        ]
