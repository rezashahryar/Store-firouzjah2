from decimal import Decimal
from rest_framework import serializers
from store import models

from .product_serializers import ProductCoverSerializer

class ProductCartItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='base_product.title_farsi')
    price_after_discount = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ['id', 'title', 'slug', 'unit_price', 'price_after_discount']

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
    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['quantity']
    

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['product', 'quantity']
    
    def create(self, validated_data):
        cart_id = self.context['cart_id']

        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try:
            cart_item = models.CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem.objects.create(cart_id=cart_id, **validated_data)
        
        self.instance = cart_item
        return cart_item

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item):
        return cart_item.product.unit_price * cart_item.quantity
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price_cart = serializers.SerializerMethodField()
    arzesh_afzoode = serializers.SerializerMethodField()
    sood_cart = serializers.SerializerMethodField()
    amount_payable = serializers.SerializerMethodField()

    class Meta:
        model = models.Cart
        fields = ['id', 'total_price_cart', 'arzesh_afzoode', 'sood_cart', 'amount_payable', 'items']
        read_only_fields = ['id']

    def get_total_price_cart(self, cart):
        return sum(item.product.unit_price * item.quantity for item in cart.items.all())
    
    def get_arzesh_afzoode(self, cart):
        return int(self.get_total_price_cart(cart) * (9 / Decimal(100)))
    
    def get_sood_cart(self, cart):
        result = 0

        for item in cart.items.all():
            if item.product.discount_percent:
                product_amount_discount = ((item.product.discount_percent / Decimal(100)) * item.product.unit_price) * item.quantity
                result += product_amount_discount
        return int(result)
    
    def get_amount_payable(self, cart):
        return self.get_total_price_cart(cart) - self.get_sood_cart(cart)