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


urlpatterns = [
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
    path('list/staff/permissions/', views.ListPermissionStaffApiView.as_view(), name='list_staff_permissions'),
    path('create/base-product/', views.CreateBaseProductApiView.as_view(), name='create_base_product'),
    path('contract/', views.ContractApiView.as_view(), name='contract'),
    path('index/', views.IndexPageApiView.as_view(), name='index'),
] + router.urls

