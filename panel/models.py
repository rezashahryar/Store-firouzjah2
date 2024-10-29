from django.db import models
from django.core.validators import validate_integer
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='profile')
    full_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=12, validators=[validate_integer])
    email = models.EmailField(null=True)


class RequestPhotographyService(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_num = models.CharField(max_length=11, validators=[validate_integer])
    province = models.ForeignKey(settings.PATH_PROVINCE_MODEL, on_delete=models.CASCADE, related_name='request_photography')
    city = models.ForeignKey(settings.PATH_CITY_MODEL, on_delete=models.CASCADE, related_name='request_photography')
    mantaghe = models.ForeignKey(settings.PATH_MANTAGHE_MODEL, on_delete=models.CASCADE, related_name='request_photography')
    address = models.TextField()
    store_name = models.CharField(max_length=255)
    request_text = models.TextField()

    def __str__(self) -> str:
        return f'{self.full_name}: {self.store_name}'
    

class Staff(models.Model):

    class GenderChoices(models.TextChoices):
        MALE = 'm', _('مرد')
        FEMALE = 'f', _('زن')

    class MaritalStatusChoices(models.TextChoices):
        SINGLE = 's', _('مجرد')
        MARRIED = 'm', _('متاهل')

    class UniversityDegreeChoices(models.TextChoices):
        DIPLOM = 'di', _('دیپلم')
        FOQ_DIPLOM = 'fd', _('فوق دیپلم') 
        LISAANS = 'l', _('لیسانس')
        FOQ_LISAANS = 'fl', _('فوق لیسانس')
        DOCTORA = 'd', _('دکترا')

    class MilitaryStatusChoices(models.TextChoices):
        MOAAF = 'm', _('معاف')

    class SkillLevelChoices(models.TextChoices):
        KHOOB = 'k', _('خوب')
        KEILY_KHOOB = 'kk', _('خیلی خوب')
        AALY = 'a', _('عالی')

    class StaffStatusChoices(models.TextChoices):
        WAITING = 'wa', _('در انتظار تایید')
        APPROVED = 'ap', _('تایید شده')
        SUSPENTION = 'su', _('تعلیق')
        NOT_APPROVED = 'na', _('عدم تایید')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff', null=True)
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    marital_status = models.CharField(max_length=1, choices=MaritalStatusChoices.choices)
    code_melly = models.CharField(max_length=10, validators=[validate_integer])
    shomare_shnasnaame = models.CharField(max_length=10, validators=[validate_integer])
    mobile_num = models.CharField(max_length=11, validators=[validate_integer])
    phone_num = models.CharField(max_length=11, validators=[validate_integer])
    email = models.EmailField()
    birth_date = models.DateField()
    university_degree = models.CharField(max_length=2, choices=UniversityDegreeChoices.choices)
    field_of_study = models.CharField(max_length=255)
    militari_status = models.CharField(max_length=2, choices=MilitaryStatusChoices.choices)
    shomare_shabaa = models.CharField(max_length=26)
    province = models.ForeignKey(settings.PATH_PROVINCE_MODEL, on_delete=models.CASCADE, related_name='staffs')
    city = models.ForeignKey(settings.PATH_CITY_MODEL, on_delete=models.CASCADE, related_name='staffs')
    mantaghe = models.ForeignKey(settings.PATH_MANTAGHE_MODEL, on_delete=models.CASCADE, related_name='staffs')
    mahalle = models.CharField(max_length=255)
    address = models.TextField()
    post_code = models.CharField(max_length=10, validators=[validate_integer])
    description = models.TextField()

    tasvire_personelly = models.ImageField(upload_to='staffs/tasvire_personelly/', null=True)
    cart_melly = models.ImageField(upload_to='staffs/cart_melly/', null=True)
    shenasnaame_image = models.ImageField(upload_to='staffs/shenasnaame_image/', null=True)
    university_degree_image = models.ImageField(upload_to='staffs/university_degree_image/', null=True)
    adame_sooe_pishine = models.ImageField(upload_to='staffs/adame_sooe_pishine/', null=True)
    cart_payan_khedmat = models.ImageField(upload_to='staffs/cart_payan_khedmat/', null=True)

    level_english = models.CharField(max_length=2, choices=SkillLevelChoices.choices)
    computer_level = models.CharField(max_length=2, choices=SkillLevelChoices.choices)
    finance_level = models.CharField(max_length=2, choices=SkillLevelChoices.choices)
    digital_marketing_level = models.CharField(max_length=2, choices=SkillLevelChoices.choices)
    photography_level = models.CharField(max_length=2, choices=SkillLevelChoices.choices)
    areas_of_cooperation_level = models.CharField(max_length=2, choices=SkillLevelChoices.choices)
    minimum_salary_requested = models.IntegerField()

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staffs', null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=2, choices=StaffStatusChoices.choices, default=StaffStatusChoices.WAITING)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('slider_settings', 'slider settings'),
            ('contract_settings', 'contract settings'),
            ('list_of_staffs', 'list of staffs'),
            ('list_of_users', 'list of users'),
            ('list_of_products (approved)', 'list of products (approved)'),
            ('list_of_products (waiting)', 'list of products (waiting)'),
            ('list_of_all_products', 'list of all products'),
            ('list_of_products (not_approved)', 'list of products (not approved)'),
            ('create_new_product', 'create new product'),
            ('list_of_stores (waiting)', 'list of stores (waiting)'),
            ('list_of_stores (approved)', 'list of stores (approved)'),
            ('list_of_stores (not_approved)', 'list of stores (not approved)'),
            ('support_of_stores', 'support of stores'),
            ('orders (delivered)', 'orders (delivered)'),
            ('list_of_customers', 'list of customers'),
            ('add_category', 'add category'),
            ('add_item', 'add item'),
            ('request_photography_service', 'request photography service'),
            ('backup', 'backup'),
            ('index_page', 'index page'),
            ('banner_settings', 'banner settings'),
            ('registration_of_staff', 'registration of staff'),
            ('request_staff', 'request staff'),
            ('contact_us', 'contact us'),
            ('list_of_all_stores', 'list of all stores'),
            ('list_of_all_orders', 'list of all orders'),
            ('list_of_return_orders', 'list of return orders'),
            ('list_of_current_orders', 'list of current orders'),
            ('list_of_canceled_orders', 'list of canceled orders'),
            ('all_categories', 'all categories'),
            ('add_product_type', 'add product type'),
            ('pages_settings', 'pages settings'),
            ('support_customers', 'support customers'),
            ('support_staffs', 'support staffs'),
            ('add_sub_category', 'add sub category'),
            ('transactions', 'transactions'),
            ('common_questions', 'common questions'),
            ('web_mail', 'web mail'),
            ('public_settings', 'public settings'),
            ('product_box_settings', 'product_box_settings'),
            ('edit_profile', 'edit profile'),
        ]

    def __str__(self) -> str:
        return self.full_name
    

class CareerRecords(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='career_records')
    company_name = models.CharField(max_length=255)
    job_position = models.CharField(max_length=255, verbose_name='پست سازمانی')
    reason_leaving_work = models.TextField()
    duration_activity_based_month = models.IntegerField()
    insurance_period_based_month = models.IntegerField()


class Page(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT, related_name='pages', null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    slug = models.SlugField(unique=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    

class CommonQuestion(models.Model):
    
    class TypeCommonQuestionChoices(models.TextChoices):
        MAIN_SUBJECT = 'ms', _('ثبت موضوع اصلی')
        QUESTION = 'q', _('پرسش')

    class MainSubjectChoices(models.TextChoices):
        REGISTER = 'r', _('ثبت نام')
        CONTRACT_WITH_FIROUZJAH = 'c', _('قرارداد با فیروزجاه')
        BILL = 'b', _('صورتحساب')
        ACCOUNT = 'a', _('حساب کاربری')

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='common_questions')
    main_subject = models.CharField(max_length=1, choices=MainSubjectChoices.choices)
    type = models.CharField(max_length=2, choices=TypeCommonQuestionChoices.choices)

    title = models.CharField(max_length=255)
    text = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    

class FeeForSellingProduct(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='selling_fees', null=True)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='selling_fees', null=True)
    
    category = models.ForeignKey('store.ProductCategory', on_delete=models.CASCADE, related_name='fees')
    sub_category = models.ForeignKey('store.ProductSubCategory', on_delete=models.CASCADE, related_name='fees')
    product_type = models.ForeignKey('store.ProductType', on_delete=models.CASCADE, related_name='fees')
    
    fee_percent = models.IntegerField()


class Contract(models.Model):
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
