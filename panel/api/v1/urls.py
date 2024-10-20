from django.urls import path
from rest_framework import routers

from . import views

# create your urls here

router = routers.DefaultRouter()

router.register('pages', views.PageViewSet, basename='pages')
router.register('common-question', views.CommonQuestionViewSet, basename='common-question')
router.register('fee-product', views.FeeForSellingProductViewSet, basename='fee_product')


urlpatterns = [
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
] + router.urls

