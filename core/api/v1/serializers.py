from rest_framework import serializers
from django.core.cache import cache
from rest_framework.authtoken.models import Token

# create your serializers here


class SendOtpSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()


class VerifyOtpSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    otp_code = serializers.CharField()

    def validate_otp_code(self, otp_code):
        if not cache.get(otp_code):
            raise serializers.ValidationError('the code has expired')
        return otp_code
    

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']
        read_only_fields = ['key']
