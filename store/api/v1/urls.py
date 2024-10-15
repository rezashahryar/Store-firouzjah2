from django.urls import path, include
from rest_framework import routers

from . import views

# create your urls here

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('list/category/', views.ProductCategoryListApiView.as_view(), name='list_category'),
    path('similar-products/<int:product_pk>/', views.ListSimmilarProductViewSet.as_view(), name='list_similar_product'),
    path('', include(router.urls)),
]

