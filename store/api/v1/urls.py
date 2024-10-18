from django.urls import path, include
from rest_framework import routers

from . import views

# create your urls here

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('list/category/', views.ProductCategoryListApiView.as_view(), name='list_category'),
    path(
        'create/product-comment/<int:product_id>/',
        views.CreateProductCommentApiView.as_view(),
        name='create_product_comment'
    ),
    path(
        'create/product-reply-comment/<int:comment_id>/',
        views.CreateProductReplyCommentApiView.as_view(),
        name='create_product_reply_comment'
    ),
    path(
        'similar-products/<int:product_pk>/',
        views.ListSimmilarProductViewSet.as_view(),
        name='list_similar_product'
    ),
    path('', include(router.urls)),
]

