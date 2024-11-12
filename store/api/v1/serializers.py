from decimal import Decimal

from rest_framework import serializers

from store import models


class ProductCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']


class ListProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')
    category = serializers.CharField(source='base_product.category')
    price_after_discount = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = [
            'id', 'category', 'title', 'slug', 'unit_price', 'inventory', 'price_after_discount', 'discount_percent', 'start_discount_datetime',
            'end_discount_datetime'
        ]

    def get_price_after_discount(self, product):
        if product.discount_percent:
            return product.unit_price - int(((product.discount_percent / Decimal(100)) * product.unit_price))
        return None
    
    def to_representation(self, instance):
        context = super().to_representation(instance)

        images = self.context['images']
        for img in images:
            if img.base_product_id == instance.base_product.pk and img.is_cover:
                img_obj = img
                context['cover'] = ProductCoverSerializer(img_obj).data
            elif not img.base_product_id == instance.base_product.pk and img.is_cover:
                continue
        return context
    

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['id', 'name', 'image']


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductBrand
        fields = ['id', 'name', 'english_name']
