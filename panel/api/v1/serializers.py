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
        if obj.user.profile.full_name:
            return obj.user.profile.full_name
        return str(obj.user)


class BaseProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()
    product_type = serializers.StringRelatedField()
    authenticity = serializers.CharField(source='get_authenticity_display')
    warranty = serializers.CharField(source='get_warranty_display')

    class Meta:
        model = store_models.BaseProduct
        fields = [
            'id', 'store', 'category', 'sub_category', 'product_type', 'title_farsi', 'title_english',
            'authenticity', 'warranty'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.ProductImage
        fields = ['image']


class ReviewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.Product
        fields = ['reviewer', 'reason']


class ProductItemDetailSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()

    class Meta:
        model = models.SetProductItem
        fields = ['item', 'value']


class ProductSerializer(serializers.ModelSerializer):
    items = ProductItemDetailSerializer(many=True)
    product_status = serializers.CharField(source='get_product_status_display')
    base_product = BaseProductSerializer()
    reviewer = serializers.StringRelatedField()
    cover = serializers.SerializerMethodField()

    class Meta:
        model = store_models.Product
        fields = [
            'id', 'base_product', 'inventory', 'unit_price', 'discount_percent', 'start_discount_datetime',
            'end_discount_datetime', 'shenaase_kaala', 'product_code', 'product_status', 'active_status',
            'datetime_created', 'datetime_modified', 'items', 'reason', 'reviewer', 'cover'
        ]

    def get_cover(self, obj):
        return ProductImageSerializer(obj.cover).data


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


class CreateBaseProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.ProductCategory
        fields = ['name']


class CreateBaseProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.ProductSubCategory
        fields = ['name']


class CreateBaseProductProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.ProductType
        fields = ['title']


class CreateBaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.BaseProduct
        fields = [
            'id', 'category', 'sub_category', 'product_type', 'title_farsi', 'title_english',
            'authenticity', 'warranty', 'shiping_method',
        ]
    
    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['category'] = CreateBaseProductCategorySerializer(instance.category).data
        context['sub_category'] = CreateBaseProductSubCategorySerializer(instance.sub_category).data
        context['product_type'] = CreateBaseProductProductTypeSerializer(instance.product_type).data
        return context

    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        if request.user.is_staff:
            fields['store'] = serializers.PrimaryKeyRelatedField(queryset=store_models.Store.objects.all())
        return fields

    def create(self, validated_data):
        return store_models.BaseProduct.objects.create(
            store_id=self.context['store_pk'],
            **validated_data
        )


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductItem
        fields = ['id', 'category', 'sub_category', 'name', 'status']

    def validate(self, attrs):
        category = attrs['category']
        sub_category = attrs['sub_category']
        name = attrs['name']
        if models.ProductItem.objects.filter(category=category,sub_category=sub_category,name=name).exists():
            raise serializers.ValidationError('موجود')
        return attrs

    def create(self, validated_data):
        product_id = self.context['product_id']
        product_obj = store_models.Product.objects.get(id=product_id)
        return models.ProductItem.objects.create(
            product_type_id=product_obj.base_product.product_type.pk,
            **validated_data
        )


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.Product
        fields = [
            'id', 'inventory', 'unit_price', 'discount_percent', 'start_discount_datetime', 'end_discount_datetime',
            'shenaase_kaala', 'barcode', 'length_package', 'width_package', 'height_package', 'weight_package',
        ]

    # def validate(self, attrs):
    #     request = self.context['request']
    #     if isinstance(request.data, list):
    #         base_product_id = request.data[0]['base_product_id']
    #         try:
    #             base_product_obj = store_models.BaseProduct.objects.get(id=base_product_id)
    #         except store_models.BaseProduct.DoesNotExist:
    #             raise serializers.ValidationError('ارور')
    #     base_product_id = request.data['base_product_id']
    #     try:
    #         base_product_obj = store_models.BaseProduct.objects.get(id=base_product_id)
    #     except store_models.BaseProduct.DoesNotExist:
    #         raise serializers.ValidationError('ارور')
    #     return attrs

    def create(self, validated_data):
        request = self.context['request']
        product = store_models.Product.objects.create(
            base_product_id=request.data[0]['base_product_id'],
            shenaase_kaala=validated_data['shenaase_kaala'],
            barcode=validated_data['barcode'],
            inventory=validated_data['inventory']
        )
        validated_data.pop('shenaase_kaala')
        validated_data.pop('barcode')
        validated_data.pop('inventory')
        list_product_items = []
        for key in validated_data:
            item = models.ProductItem.objects.get(name=key)
            models.SetProductItem.objects.create(
                product_id=product.pk,
                item_id=item.pk,
                value=validated_data[key],
            )

        return product
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        base_product_id = request.data[0]['base_product_id']
        try:
            base_product_obj = store_models.BaseProduct.objects.get(id=base_product_id)
        except store_models.BaseProduct.DoesNotExist:
            raise serializers.ValidationError('ارور')
        items = models.ProductItem.objects.filter(product_type_id=base_product_obj.product_type.pk)
        for item in items:
            fields[item.name] = serializers.CharField()

        return fields


class ProductDetailItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = store_models.Product
        fields = ['title']

    def get_title(self, product):
        return product.base_product.title_farsi
    

class SetProductItemFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductItem
        fields = ['name']


class SetProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SetProductItem
        fields = ['id', 'product', 'item', 'value']

    def validate(self, attrs):
        if models.SetProductItem.objects.filter(product=attrs['product'], item=attrs['item']).exists():
            raise serializers.ValidationError('موجود')
        if attrs['item'].product_type != attrs['product'].base_product.product_type:
            raise serializers.ValidationError('ارور')
        return attrs
    
    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['product'] = ProductDetailItemSerializer(instance.product).data
        context['item'] = SetProductItemFieldSerializer(instance.item).data
        return context


class OrderItemSerializer(serializers.ModelSerializer):
    # product_code = serializers.SerializerMethodField()

    class Meta:
        model = store_models.OrderItem
        fields = ['id']

    # def get_product_code(self, order_item):
    #     return order_item.product.product_code


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


class CreateFeeForSellingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeeForSellingProduct
        fields = ['id', 'category', 'sub_category', 'product_type', 'fee_percent']


class FeeForSellingProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()
    product_type = serializers.StringRelatedField()

    class Meta:
        model = models.FeeForSellingProduct
        fields = ['id', 'category', 'sub_category', 'product_type', 'fee_percent']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context['request']
        if request.user.is_staff:
            fields['staff'] = serializers.CharField()
            fields['datetime_modified'] = serializers.DateTimeField()
        elif request.user.store:
            fields['store'] = serializers.CharField()
        return fields

    def create(self, validated_data):
        user_id = self.context['user_id']
        user = User.objects.get(id=user_id)

        fee_obj = models.FeeForSellingProduct(
            category=validated_data['category'],
            sub_category=validated_data['sub_category'],
            product_type=validated_data['product_type'],
            fee_percent=validated_data['fee_percent'],
        )
        if user.is_staff:
            fee_obj.staff_id = user.staff.pk
        else:
            fee_obj.store_id = user.store.pk
        fee_obj.save()

        return fee_obj
    

class CreateProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.ProductCategory
        fields = ['id', 'name', 'slug', 'image']
        read_only_fields = ['slug']


class CreateProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.ProductSubCategory
        fields = ['id', 'category', 'name', 'slug', 'image']
        read_only_fields = ['slug']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.ProductType
        fields = ['id', 'category', 'sub_category', 'title']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = store_models.Customer
        fields = ['user']
