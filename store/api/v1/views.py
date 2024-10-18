from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import generics
from rest_framework import mixins
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated

from store import models

from . import serializers

# create your views here


class ListSimmilarProductViewSet(generics.ListAPIView):
    serializer_class = serializers.SimilarProductSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_pk']
        product_obj = get_object_or_404(models.Product, id=product_id)
        queryset = models.SimilarProduct.objects.filter(
            product__base_product__product_type=product_obj.base_product.product_type
        ).exclude(product_id=product_id)
        return queryset


class ProductCategoryListApiView(generics.ListAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = models.Product.objects.select_related('base_product__category') \
            .select_related('base_product__sub_category').prefetch_related(Prefetch(
                'base_product__properties',
                queryset=models.SetProductProperty.objects.select_related('property')
        )).select_related('base_product__store').all()

        if self.action == 'list':
            return queryset.defer(
                'inventory', 'unit', 'size','length_package', 'width_package', 'height_package',
                'weight_package', 'shenaase_kaala', 'barcode', 'product_status', 'active_status',
                'reason', 'base_product__title_english', 'base_product__product_code',
                'base_product__authenticity', 'base_product__warranty','base_product__shiping_method',
                'base_product__category__image', 'base_product__category__slug'
            )
        
        return queryset.prefetch_related(
            Prefetch(
                'base_product__comments',
                queryset=models.ProductComment.objects.select_related('user').prefetch_related(
                    Prefetch(
                        'replies',
                        queryset=models.ProductReplyComment.objects.select_related('user')
                    )
                )
            )
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer
    
    def get_serializer_context(self):
        return {
            'images': models.ProductImage.objects.all()
        }
    

class CreateProductCommentApiView(generics.CreateAPIView):
    queryset = models.ProductComment.objects.all()
    serializer_class = serializers.ProductCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.pk,
            'product_id': self.kwargs['product_id']
        }
    

class CreateProductReplyCommentApiView(generics.CreateAPIView):
    queryset = models.ProductReplyComment
    serializer_class = serializers.ProductReplyCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.pk,
            'comment_id': self.kwargs['comment_id']
        }
    

class CartViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.prefetch_related(Prefetch(
        'items',
        queryset=models.CartItem.objects.select_related('product__base_product')
    )).all()

    def get_serializer_context(self):
        return {'images': models.ProductImage.objects.all()}
