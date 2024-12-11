from rest_framework import serializers
from django.utils.text import slugify

from store import models as store_models


class AddProductCategorySerializer(serializers.ModelSerializer):
    link = serializers.CharField()

    class Meta:
        model = store_models.ProductCategory
        fields = ['name', 'image', 'link']

    def create(self, validated_data):
        print(validated_data)
        user_id = self.context['user_id']
        return store_models.ProductCategory.objects.create(
            user_creator_id=user_id,
            name=validated_data['name'],
            slug=slugify(validated_data['link'], allow_unicode=True),
            image=validated_data['image']
        )
    

class ProductCategorySerializer(serializers.ModelSerializer):
    user_creator = serializers.StringRelatedField()
    class Meta:
        model = store_models.ProductCategory
        fields = ['user_creator', 'name', 'slug', 'image']
