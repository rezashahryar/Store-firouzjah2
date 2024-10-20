from django.urls import path

from . import views

# create your urls here


urlpatterns = [
    path('profile/', views.ProfileApiView.as_view(), name='profile'),
]

