from django.urls import path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')
router.register('cart', views.CartViewSet, basename='carts')

product_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_routers.register('comments', views.ProductCommentViewSet, basename='comments')
product_routers.register('similar-products', views.SimilarProductsViewSet, basename='similar-products')
product_routers.register('report', views.SendReportProductViewSet, basename='report-product')

comments_router = routers.NestedDefaultRouter(product_routers, 'comments', lookup='comment')
comments_router.register('replies', views.ProductReplyCommentViewSet, basename='replies_comments')

cart_item_routers = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_item_routers.register('items', views.CartItemViewSet, basename='cart_items')


urlpatterns = [
    path('list/categories/', views.ProductCategoryListApiView.as_view(), name='list_categories'),
    path('list/brands/', views.ProductBrandListApiView.as_view(), name='list_brands'),
] + router.urls + product_routers.urls + comments_router.urls + cart_item_routers.urls

