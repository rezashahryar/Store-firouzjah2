from django.urls import path
from rest_framework import routers

from . import views

# create your urls here

router = routers.DefaultRouter()

router.register('pages', views.PageViewSet, basename='pages')
router.register('common-question', views.CommonQuestionViewSet, basename='common-question')
router.register('fee-product', views.FeeForSellingProductViewSet, basename='fee_product')
router.register('orders', views.OrderViewSet, basename='orders')
router.register('users', views.UserViewSet, basename='users')
router.register('staffs', views.StaffViewSet, basename='staff')
router.register('products', views.ProductViewSet, basename='products')
router.register('product/categories', views.ProductCategoryViewSet, basename='product-category')
router.register('product/sub-categories', views.ProductSubCategoryViewSet, basename='product-sub-category')
router.register('product-type', views.ProductTypeViewSet, basename='product_type')
router.register('customers', views.CustomerViewSet, basename='customers')


urlpatterns = [
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
    path('list/all-staff/permissions/', views.ListAllPermissionStaffApiView.as_view(), name='list_staff_permissions'),
    path('create/base-product/', views.CreateBaseProductApiView.as_view(), name='create_base_product'),
    path('contract/', views.ContractApiView.as_view(), name='contract'),
    path('index/', views.IndexPageApiView.as_view(), name='index'),
    path('list/product-items/', views.ListProductItemApiView.as_view(), name='list_product_item'),
    path('set-item/', views.SetProductItemApiView.as_view(), name='set-product-item'),
] + router.urls
