from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from core.models import User
from panel import models
from store import models as store_models

# create your serializers here


class StoreSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = store_models.Store
        fields = [
            'user', 'store_code'
        ]

    def get_user(self, obj):
        return obj.user.profile.full_name


class BaseProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer()

    class Meta:
        model = store_models.BaseProduct
        fields = [
            'id', 'store'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.ProductImage
        fields = ['image']


class ReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.Product
        fields = ['reviewer', 'reason']


class ProductSerializer(serializers.ModelSerializer):
    product_status = serializers.CharField(source='get_product_status_display')
    base_product = BaseProductSerializer()
    category = serializers.CharField(source='base_product.category')
    sub_category = serializers.CharField(source='base_product.sub_category')
    product_type = serializers.CharField(source='base_product.product_type')
    title_farsi = serializers.CharField(source='base_product.title_farsi')
    title_english = serializers.CharField(source='base_product.title_english')
    authenticity = serializers.CharField(source='base_product.get_authenticity_display')
    warranty = serializers.CharField(source='base_product.get_warranty_display')

    class Meta:
        model = store_models.Product
        fields = [
            'id', 'base_product', 'category', 'sub_category', 'product_type', 'title_farsi', 'title_english',
            'inventory', 'product_code', 'unit_price', 'discount_percent', 'start_discount_datetime',
            'end_discount_datetime', 'authenticity', 'warranty', 'shenaase_kaala', 'product_status', 'active_status',
            'datetime_created',
        ]

    def to_representation(self, instance):
        context = super().to_representation(instance)

        images = self.context['images']
        for img in images:
            if img.base_product_id == instance.base_product.pk and img.is_cover:
                img_obj = img
                context['cover'] = ProductImageSerializer(img_obj).data
            elif not img.base_product_id == instance.base_product.pk and img.is_cover:
                continue

        return context


class UpdateStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Staff
        fields = ['status', 'reason']


class CreateStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Staff
        fields = [
            'full_name', 'father_name', 'gender', 'marital_status', 'code_melly', 'shomare_shnasnaame',
            'mobile_num', 'phone_num', 'email', 'birth_date', 'university_degree', 'field_of_study',
            'militari_status', 'shomare_shabaa', 'province', 'city', 'mantaghe', 'mahalle', 'address',
            'post_code', 'description', 'tasvire_personelly', 'cart_melly', 'shenasnaame_image', 'university_degree_image', 'adame_sooe_pishine', 'cart_payan_khedmat',
            'level_english', 'computer_level', 'finance_level', 'digital_marketing_level', 'photography_level', 'areas_of_cooperation_level', 'minimum_salary_requested',
            'reviewer', 'reason', 'status', 'datetime_created'
        ]
        read_only_fields = ['reviewer', 'reason']
    
    def validate(self, attrs):
        user_id = self.context['user_id']
        if models.Staff.objects.filter(user_id=user_id).exists():
            raise serializers.ValidationError('کاربری از قبل با این ایمیل در سایت ثبت نام کرده است. هر کاربر مجاز به داشتن تنها یک فروشگاه می باشد')
        return attrs
    
    def create(self, validated_data):
        staff = models.Staff.objects.create(
            user_id=self.context['user_id'],
            **validated_data
        )
        staff.user.is_staff = True
        staff.user.save()
        return staff


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class StaffSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    marital_status = serializers.CharField(source='get_marital_status_display')
    university_degree = serializers.CharField(source='get_university_degree_display')
    militari_status = serializers.CharField(source='get_militari_status_display')
    level_english = serializers.CharField(source='get_level_english_display')
    computer_level = serializers.CharField(source='get_computer_level_display')
    finance_level = serializers.CharField(source='get_finance_level_display')
    digital_marketing_level = serializers.CharField(source='get_digital_marketing_level_display')
    photography_level = serializers.CharField(source='get_photography_level_display')
    areas_of_cooperation_level = serializers.CharField(source='get_areas_of_cooperation_level_display')
    status = serializers.CharField(source='get_status_display')
    province = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    mantaghe = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = models.Staff
        fields = [
            'id', 'user', 'full_name', 'father_name', 'gender', 'marital_status', 'code_melly', 'shomare_shnasnaame',
            'mobile_num', 'phone_num', 'email', 'birth_date', 'university_degree', 'field_of_study',
            'militari_status', 'shomare_shabaa', 'province', 'city', 'mantaghe', 'mahalle', 'address',
            'post_code', 'description', 'tasvire_personelly', 'cart_melly', 'shenasnaame_image', 'university_degree_image', 'adame_sooe_pishine', 'cart_payan_khedmat',
            'level_english', 'computer_level', 'finance_level', 'digital_marketing_level', 'photography_level', 'areas_of_cooperation_level', 'minimum_salary_requested',
            'reviewer', 'reason', 'status', 'datetime_created', 'permissions'
        ]
    
    def get_permissions(self, staff):
        return PermissionSerializer(staff.user.user_permissions.all(), many=True).data


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['pk', 'email', 'date_joined']


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contract
        fields = ['text']


class CreateBaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.BaseProduct
        fields = [
            'category', 'sub_category', 'product_type', 'title_farsi', 'title_english',
            'authenticity', 'warranty', 'shiping_method',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_code = serializers.SerializerMethodField()

    class Meta:
        model = store_models.OrderItem
        fields = ['product_code']

    def get_product_code(self, order_item):
        return order_item.product.product_code


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = store_models.Order
        fields = ['tracking_code', 'items']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ['full_name', 'mobile', 'email']


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Page
        fields = ['id', 'title', 'text', 'slug']

    def create(self, validated_data):
        return models.Page.objects.create(
            staff_id=self.context['staff_id'],
            **validated_data
        )
    

class CreateCommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommonQuestion
        fields = ['type', 'main_subject', 'title', 'text']

    def create(self, validated_data):
        return models.CommonQuestion.objects.create(
            staff_id=self.context['staff_id'],
            **validated_data
        )


class CommonQuestionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    main_subject = serializers.CharField(source='get_main_subject_display')

    class Meta:
        model = models.CommonQuestion
        fields = ['id', 'type', 'main_subject', 'title', 'text']


class FeeForSellingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeeForSellingProduct
        fields = ['id', 'category', 'sub_category', 'product_type', 'fee_percent']
