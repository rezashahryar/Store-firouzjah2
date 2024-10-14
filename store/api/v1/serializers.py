from rest_framework import serializers

from store import models

# create your serializers here


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['name', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']


class ProductPropertiesSerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField()
    class Meta:
        model = models.SetProductProperty
        fields = ['property', 'value']


class BaseProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    properties = ProductPropertiesSerializer(many=True)

    class Meta:
        model = models.BaseProduct
        fields = [
            'title_farsi', 'title_english', 'product_code', 'images', 'properties'
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

    def to_representation(self, instance):
        context = super().to_representation(instance)

        images = self.context['images']
        for img in images:
            if img.base_product_id == instance.base_product.pk and img.is_cover:
                img_obj = img
                context['cover'] = ProductImageSerializer(img_obj).data
            elif not img.base_product_id == instance.base_product.pk and img.is_cover:
                continue
        
        # try:
        #     cover = models.ProductImage.objects.get(base_product_id=instance.base_product.pk, is_cover=True)
        # except models.ProductImage.DoesNotExist:
        #     cover = None
        # context['cover'] = ProductImageSerializer(cover).data

        return context
