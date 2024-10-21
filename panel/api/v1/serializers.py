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


class CommonQuestionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    main_subject = serializers.CharField(source='get_main_subject_display')
    
    class Meta:
        model = models.CommonQuestion
        fields = ['type', 'main_subject', 'title', 'text']
