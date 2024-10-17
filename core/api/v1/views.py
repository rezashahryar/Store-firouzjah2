import random

from rest_framework import generics
from rest_framework.response import Response

from core.mail import send_otp_code

from core.models import RequestOtp
from .serializers import SendOtpSerializer

# create your views here

class SendOtpApiView(generics.GenericAPIView):
    serializer_class = SendOtpSerializer

    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = random.randint(1000, 9999)
        
        req_otp_obj = RequestOtp.objects.create(
            email=email,
            otp_code=otp_code,
        )

        send_otp_code(request, email, otp_code)
        response_serializer = SendOtpSerializer(req_otp_obj)

        return Response(response_serializer.data)
    

class CheckOtpView(generics.GenericAPIView):
    serializer_class = ...

    def post(self, request):
        ...
