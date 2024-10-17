from rest_framework import serializers

from core.models import RequestOtp

# create your serializers here


class SendOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestOtp
        fields = ['id', 'email']
        read_only_fields = ['id']
