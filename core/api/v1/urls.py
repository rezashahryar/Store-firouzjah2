from django.urls import path

from . import views

# create your urls here

urlpatterns = [
    path('send-otp/', views.SendOtpApiView.as_view(), name='send-otp'),
]

