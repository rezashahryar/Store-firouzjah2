from django.urls import path, include
from . import views

urlpatterns = [
    path('index/', views.IndexApiView.as_view(), name='index'),
    path('add/product/category/', views.AddProductCategoryApiView.as_view(), name='add_category'),
]

