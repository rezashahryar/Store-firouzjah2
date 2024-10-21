from rest_framework import serializers

from panel import models

# create your serializers here


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['full_name', 'mobile', 'email']


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ['id', 'title', 'text']
