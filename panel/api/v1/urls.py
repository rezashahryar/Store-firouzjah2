from django.urls import path
from rest_framework import routers

from . import views

# create your urls here

router = routers.DefaultRouter()

router.register('pages', views.PageViewSet, basename='pages')


urlpatterns = [
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
] + router.urls

