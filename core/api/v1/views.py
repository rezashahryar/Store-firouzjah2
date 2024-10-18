import random

from uuid import uuid4

from rest_framework import generics
from rest_framework.response import Response
from django.core.cache import cache

from core.mail import send_otp_code
from core.models import User

from .serializers import SendOtpSerializer, VerifyOtpSerializer, UserTokenSerializer

# create your views here

class SendOtpApiView(generics.GenericAPIView):
    serializer_class = SendOtpSerializer

    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = random.randint(1000, 9999)
        
        cache_data = {
            'id': uuid4(),
            'email': email,
            'otp_code': otp_code,
        }

        cache.set(otp_code, cache_data, timeout=60 * 3)
        send_otp_code(request, email, otp_code)
        return Response(SendOtpSerializer(cache_data).data)
    

class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer

    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cache.get(serializer.validated_data['otp_code'])
        try:
            user = User.objects.get(email=data['email'])
            user_token = user.auth_token
            return Response(UserTokenSerializer(user_token).data)
        except User.DoesNotExist:
            user = User.objects.create(email=data['email'])
            user.save()
            user.username = f'user_{user.pk}'
            user.save()

            user_token = user.auth_token
            return Response(UserTokenSerializer(user_token).data)


