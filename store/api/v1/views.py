from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import generics
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models import Count, Prefetch
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from panel.models import SetProductItem
from store import models

from . import serializers
from .paginations import ListProductPagination
from .filters import ListProductFilter


class ProductViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['base_product__title_farsi']
    filterset_class = ListProductFilter
    ordering_fields = ['datetime_created', 'unit_price', 'count_sell']
    pagination_class = ListProductPagination
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = models.Product.approved.select_related('base_product__category') \
            .select_related('base_product__sub_category').all()
        if self.action == 'retrieve':
            return queryset.prefetch_related(Prefetch(
                'items',
                queryset=SetProductItem.objects.select_related('item')
            )).select_related('base_product__store').prefetch_related('base_product__images') \
            .prefetch_related(Prefetch(
                'base_product__comments',
                queryset=models.ProductComment.objects.select_related('user').prefetch_related(Prefetch(
                    'replies',
                    queryset=models.ProductReplyComment.objects.select_related('user')
                ))
            ))
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ProductDetailSerializer
        return serializers.ListProductSerializer

    def filter_queryset(self, queryset):
        ordering = self.request.GET.get("ordering", None)
        # ordering by property field
        if ordering is not None:
            if ordering == 'count_sell':
                queryset = queryset.annotate(count_selll=Count('order_items')).order_by('count_selll')
            if ordering == '-count_sell':
                queryset = queryset.annotate(count_selll=Count('order_items')).order_by('-count_selll')
            return queryset
        
        return super().filter_queryset(queryset)

    def get_serializer_context(self):
        return {'images': models.ProductImage.objects.all()}
    

class SimilarProductsViewSet(ModelViewSet):
    serializer_class = serializers.SimilarProductSerializer

    def get_queryset(self):
        product_obj = models.Product.approved.select_related('base_product').get(slug=self.kwargs['product_slug'])
        queryset = models.SimilarProduct.objects.select_related('product__base_product') \
            .select_related('store').filter(
                product__base_product__title_farsi__icontains=product_obj.base_product.title_farsi
            )
        return queryset
    

class SendReportProductViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                            GenericViewSet):
    serializer_class = serializers.SendReportProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.ReportProduct.objects.filter(product__slug=self.kwargs['product_slug'])

    def get_serializer_context(self):
        return {'product_slug': self.kwargs['product_slug'], 'user_id': self.request.user.pk}
    

class ProductCategoryListApiView(generics.ListAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.ProductCategorySerializer


class ProductBrandListApiView(generics.ListAPIView):
    queryset = models.ProductBrand.objects.all()
    serializer_class = serializers.ProductBrandSerializer


class ProductCommentViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    serializer_class = serializers.ProductCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']

        product_obj = models.Product.objects.select_related('base_product') \
            .filter(slug=product_slug).values('base_product_id')
        
        return models.ProductComment.objects.select_related('product') \
            .select_related('user').filter(product_id__in=product_obj)

    def get_serializer_context(self):
        return {'user_id': self.request.user.pk, 'product_id': self.kwargs['product_slug']}
    

class ProductReplyCommentViewSet(ModelViewSet):
    queryset = models.ProductReplyComment.objects.all()
    serializer_class = serializers.ProductReplyCommentSerializer

    def get_queryset(self):
        comment_pk = self.kwargs['comment_pk']
        return models.ProductReplyComment.objects.select_related('user').filter(comment_id=comment_pk)
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.pk, 'comment_id': self.kwargs['comment_pk']}
    

class CartViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = models.Cart.objects.prefetch_related(Prefetch(
        'items',
        queryset=models.CartItem.objects.select_related('product__base_product') \
            .defer(
                'product__product_code', 'product__inventory', 'product__start_discount_datetime', 'product__reason',
                'product__end_discount_datetime', 'product__datetime_modified', 'product__active_status',
                'product__datetime_created', 'product__reviewer_id', 'product__product_status', 'product__width_package',
                'product__barcode', 'product__shenaase_kaala', 'product__weight_package', 'product__height_package',
                'product__length_package', 'product__base_product__category', 'product__base_product__sub_category',
                'product__base_product__store', 'product__base_product__product_type', 'product__base_product__brand',
                'product__base_product__title_english', 'product__base_product__description',
                'product__base_product__authenticity', 'product__base_product__warranty', 'product__base_product__shiping_method',
            )
    )).all()
    serializer_class = serializers.CartSerializer

    def get_serializer_context(self):
        return {'images': models.ProductImage.objects.all()}
    

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return models.CartItem.objects.select_related('product__base_product') \
            .filter(cart_id=cart_pk).defer(
                'product__product_code', 'product__inventory', 'product__start_discount_datetime', 'product__reason',
                'product__end_discount_datetime', 'product__datetime_modified', 'product__active_status',
                'product__datetime_created', 'product__reviewer_id', 'product__product_status', 'product__width_package',
                'product__barcode', 'product__shenaase_kaala', 'product__weight_package', 'product__height_package',
                'product__length_package', 'product__base_product__category', 'product__base_product__sub_category',
                'product__base_product__store', 'product__base_product__product_type', 'product__base_product__brand',
                'product__base_product__title_english', 'product__base_product__description',
                'product__base_product__authenticity', 'product__base_product__warranty', 'product__base_product__shiping_method',
            )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer

    def get_serializer_context(self):
        return {'images': models.ProductImage.objects.all(), 'cart_id': self.kwargs['cart_pk']}
