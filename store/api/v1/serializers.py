from rest_framework import serializers

from store import models

# create your serializers here


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['name', 'image', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']


class ProductPropertiesSerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField()
    class Meta:
        model = models.SetProductProperty
        fields = ['property', 'value']


class ShipingRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShipingRange
        fields = ['name']


class ShipingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShipingMethod
        fields = ['name']


class ShipingPropertySerializer(serializers.ModelSerializer):
    shiping_range = ShipingRangeSerializer(many=True)
    shiping_method = ShipingMethodSerializer(many=True)
    class Meta:
        model = models.ShipingProperty
        fields = ['shiping_range', 'shiping_method']


class BaseProductFieldStoreSerializer(serializers.ModelSerializer):
    shiping_property = ShipingPropertySerializer(many=True)

    class Meta:
        model = models.Store
        fields = ['store_name', 'shiping_property']


class ProductReplyCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = models.ProductReplyComment
        fields = ['user', 'text', 'datetime_created']


class CommentSerializer(serializers.ModelSerializer):
    replies = ProductReplyCommentSerializer(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = models.ProductComment
        fields = ['user', 'text', 'datetime_created', 'replies']


class BaseProductDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    store = BaseProductFieldStoreSerializer()
    images = ProductImageSerializer(many=True)
    properties = ProductPropertiesSerializer(many=True)
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()

    class Meta:
        model = models.BaseProduct
        fields = [
            'id', 'store', 'category', 'sub_category', 'title_farsi', 'title_english', 'product_code',
            'images', 'properties', 'comments'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    base_product = BaseProductDetailSerializer()
    unit = serializers.CharField(source='get_unit_display')
    
    class Meta:
        model = models.Product
        fields = [
            'id', 'base_product', 'size', 'inventory', 'unit', 'unit_price', 'discount_percent',
            'start_discount_datetime', 'end_discount_datetime'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')
    category = serializers.CharField(source='base_product.category')

    class Meta:
        model = models.Product
        fields = [
            'id', 'title', 'category', 'slug', 'unit_price', 'discount_percent', 'start_discount_datetime',
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
    

class SimilarStoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = ['id', 'store_name', 'store_code']
    

class SimilarProductDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')

    class Meta:
        model = models.Product
        fields = [
            'id', 'title', 'discount_percent', 'unit_price', 'start_discount_datetime', 'end_discount_datetime',
            'datetime_created'
        ]
    

class SimilarProductSerializer(serializers.ModelSerializer):
    store = SimilarStoreDetailSerializer()
    product = SimilarProductDetailSerializer()

    class Meta:
        model = models.SimilarProduct
        fields = [
            'store', 'product'
        ]


class CartProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')

    class Meta:
        model = models.Product
        fields = ['title', 'slug', 'unit_price', 'discount_percent']

    def to_representation(self, instance):
        context = super().to_representation(instance)

        images = self.context['images']
        for img in images:
            if img.base_product_id == instance.base_product.pk and img.is_cover:
                img_obj = img
                context['cover'] =ProductImageSerializer(img_obj).data
            elif not img.base_product_id == instance.base_product.pk and img.is_cover:
                continue

        return context


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['total_price', 'product', 'quantity']

    def get_total_price(self, obj):
        return obj.product.unit_price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price_of_cart = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'total_price_of_cart', 'items']
        read_only_fields = ['id']

    def get_total_price_of_cart(self, obj):
        return sum(item.product.unit_price * item.quantity for item in obj.items.all())
    

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductComment
        fields = ['text']

    def create(self, validated_data):
        return models.ProductComment.objects.create(
            user_id=self.context['user_id'],
            product_id=self.context['product_id'],
            **validated_data
        )
    

class ProductReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductReplyComment
        fields = ['text']

    def create(self, validated_data):
        return models.ProductReplyComment.objects.create(
            comment_id=self.context['comment_id'],
            user_id=self.context['user_id'],
            **validated_data
        )
