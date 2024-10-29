from decimal import Decimal

from rest_framework import serializers
from django.db import transaction

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
            'id', 'store', 'category', 'sub_category', 'title_farsi', 'title_english',
            'images', 'properties', 'comments'
        ]


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductColor
        fields = ['name', 'code_color']


class ProductDetailSerializer(serializers.ModelSerializer):
    base_product = BaseProductDetailSerializer()
    unit = serializers.CharField(source='get_unit_display')
    color = ProductColorSerializer()
    
    class Meta:
        model = models.Product
        fields = [
            'id', 'base_product', 'size', 'color', 'inventory', 'unit', 'unit_price', 'discount_percent',
            'product_code', 'start_discount_datetime', 'end_discount_datetime'
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
        read_only_fields = ['slug']

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
    amount_discount = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['id', 'total_price', 'amount_discount', 'quantity', 'product']

    def get_total_price(self, obj):
        return obj.product.unit_price * obj.quantity
    
    def get_amount_discount(self, cart_item):
        if cart_item.product.discount_percent:
            return int((cart_item.product.discount_percent / Decimal(100)) * self.get_total_price(cart_item))
        return 0
    

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_pk = self.context['cart_pk']
        product = validated_data.get('product')
        quantity = validated_data['quantity']

        # if models.CartItem.objects.filter(cart_id=cart_pk, product_id=product.pk).exists():
        #     cart_item = models.CartItem.objects.get(cart_id=cart_pk, product_id=product.pk)
        #     cart_item.quantity += quantity
        #     cart_item.save()
        # else:
        #     cart_item = models.CartItem.objects.create(cart_id=cart_pk, **validated_data)

        try:
            cart_item = models.CartItem.objects.get(cart_id=cart_pk, product_id=product.pk)
            cart_item.quantity += quantity
            cart_item.save()
        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem.objects.create(cart_id=cart_pk, **validated_data)

        self.instance = cart_item

        return cart_item
    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price_of_cart = serializers.SerializerMethodField()
    arzesh_afzoode = serializers.SerializerMethodField()
    sood_cart = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'total_price_of_cart', 'arzesh_afzoode', 'sood_cart', 'items']
        read_only_fields = ['id']

    def get_total_price_of_cart(self, cart):
        return sum(item.product.unit_price * item.quantity for item in cart.items.all())
    
    def get_arzesh_afzoode(self, cart):
        return int((self.get_total_price_of_cart(cart) * 9) / 100)
    
    def get_sood_cart(self, cart):
        result = 0

        for item in cart.items.all():
            if item.product.discount_percent:
                product_amount_discount = ((item.product.discount_percent / Decimal(100)) * item.product.unit_price) * item.quantity
                result += product_amount_discount
        return int(result)


class CreateOrderSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField()

    class Meta:
        model = models.Order
        fields = [
            'id', 'cart_id', 'full_name_recipient', 'mobile_recipient', 'email_recipient', 'province', 'city', 'mantaghe',
            'mahalle', 'address', 'pelaak', 'vaahed', 'post_code', 'referrer_code', 'datetime_created'
        ]

    def validate_cart_id(self, cart_id):
        try:
            if models.Cart.objects.prefetch_related('items').get(id=cart_id).items.count() == 0:
                raise serializers.ValidationError('کارت شما فاقد محصول میباشد')
        except models.Cart.DoesNotExist:
            raise serializers.ValidationError('سبد خریدی با این آیدی موجود نیست')
        
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            data = self.validated_data

            cart_id = data['cart_id']
            cart_obj = models.Cart.objects.get(id=cart_id)

            user_id = self.context['user_id']

            customer_obj = models.Customer.objects.get(user_id=user_id)

            order = models.Order(
                customer_id=customer_obj.pk,
                full_name_recipient=data['full_name_recipient'],
                mobile_recipient=data['mobile_recipient'],
                email_recipient=data['email_recipient'],
                province=data['province'],
                city=data['city'],
                mantaghe=data['mantaghe'],
                mahalle=data['mahalle'],
                address=data['address'],
                pelaak=data['pelaak'],
                vaahed=data['vaahed'],
                post_code=data['post_code'],
                referrer_code=data['referrer_code'],
            )
            order.save()

            cart_items = models.CartItem.objects.select_related('product__base_product').filter(cart_id=cart_id)

            list_of_order_items = [
                models.OrderItem(
                    order_id=order.pk,
                    product_id=cart_item.product_id,
                    purchased_price=cart_item.product.unit_price,
                    quantity=cart_item.quantity
                ) for cart_item in cart_items
            ]

            # for item in cart_items:
            #     order_item = models.OrderItem(
            #         order_id=order.pk,
            #         product_id=item.product_id,
            #         purchased_price=item.product.unit_price,
            #         quantity=item.quantity
            #     )
            #     list_of_order_items.append(order_item)

            models.OrderItem.objects.bulk_create(list_of_order_items)

            self.instance = order

            return order

        # cart_obj.objects.delete()


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = models.OrderItem
        fields = ['product', 'purchased_price', 'quantity']


class ResponseCreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['datetime_created', 'tracking_code']
        read_only_fields = ['tracking_code']
        


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
