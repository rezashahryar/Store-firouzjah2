from rest_framework import serializers

from panel.models import SetProductItem

from store import models


class ProductCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']


class ShipingRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShipingRange
        fields = ['name']


class ShipingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShipingMethod
        fields = ['name']


class StoreShipingRangeSerializer(serializers.ModelSerializer):
    shiping_range = ShipingRangeSerializer(many=True)
    shiping_method = ShipingMethodSerializer(many=True)
    
    class Meta:
        model = models.ShipingProperty
        fields = ['shiping_range', 'shiping_method']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']


class ProductReplyCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = models.ProductReplyComment
        fields = ['id', 'user', 'text', 'datetime_created']

    def create(self, validated_data):
        comment_id = self.context['comment_id']
        user_id = self.context['user_id']
        return models.ProductReplyComment.objects.create(
            user_id=user_id,
            comment_id=comment_id,
            **validated_data
        )


class ProductCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    replies = ProductReplyCommentSerializer(many=True)

    class Meta:
        model = models.ProductComment
        fields = ['id', 'user', 'text', 'datetime_created', 'replies']

    def create(self, validated_data):
        user_id = self.context['user_id']
        product_id = self.context['product_id']
        product_obj = models.Product.objects.get(id=product_id)
        return models.ProductComment.objects.create(
            user_id=user_id,
            product_id=product_obj.base_product.pk,
            **validated_data
        )


class BaseProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()
    store_code = serializers.CharField(source='store.store_code')
    store_name = serializers.CharField(source='store.store_name')
    shiping_range = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True)
    comments = ProductCommentSerializer(many=True)

    class Meta:
        model = models.BaseProduct
        fields = [
            'id', 'category', 'sub_category', 'store_code', 'store_name', 'shiping_range', 'title_farsi',
            'title_english', 'description', 'images', 'comments'
        ]

    def get_shiping_range(self, base_product):
        return StoreShipingRangeSerializer(base_product.store.shiping_property.all(), many=True).data


class ProductItemSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()

    class Meta:
        model = SetProductItem
        fields = ['item', 'value']


class ProductDetailSerializer(serializers.ModelSerializer):
    items = ProductItemSerializer(many=True)
    base_product = BaseProductDetailSerializer()
    price_after_discount = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = [
            'id', 'base_product', 'inventory', 'product_code', 'unit_price', 'price_after_discount',
            'discount_percent', 'start_discount_datetime', 'end_discount_datetime', 'items'
        ]

    def get_price_after_discount(self, product):
        return product.price_after_discount


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
        return product.price_after_discount
    
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


class SimilarProductSerializer(serializers.ModelSerializer):
    store_code = serializers.CharField(source='store.store_code')
    product_title = serializers.CharField(source='product.base_product.title_farsi')
    unit_price = serializers.CharField(source='product.unit_price')
    datetime_created = serializers.DateTimeField(source='product.datetime_created')
    price_after_discount = serializers.SerializerMethodField()

    class Meta:
        model = models.SimilarProduct
        fields = ['id', 'store_code', 'product_title', 'unit_price', 'price_after_discount', 'datetime_created']

    def get_price_after_discount(self, similar_product):
        return similar_product.product.price_after_discount
    

class SendReportProductSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = models.ReportProduct
        fields = ['id', 'user', 'text']

    def create(self, validated_data):
        product = models.Product.objects.get(slug=self.context['product_slug'])
        return models.ReportProduct.objects.create(
            user_id=self.context['user_id'],
            product_id=product.pk,
            **validated_data
        )