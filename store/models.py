from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, validate_integer
from django.conf import settings

from .model_fields import ProductSize
# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    

class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    

class Mantaghe(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Store(models.Model):

    class StoreType(models.TextChoices):
        HAGHIGHY = 'ha', _('حقیقی')
        HOGHOUGHY = 'ho', _('حقوقی')

    store_name = models.CharField(max_length=255)

    email = models.EmailField()
    shabaa_num = models.CharField(max_length=55)

    mobile_num = models.CharField(max_length=12, validators=[validate_integer])
    phone_num = models.CharField(max_length=12, validators=[validate_integer])

    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='stores')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='stores')
    mantaghe = models.ForeignKey(Mantaghe, on_delete=models.CASCADE, related_name='stores')
    mahalle = models.CharField(max_length=255)
    address = models.TextField()
    post_code = models.CharField(max_length=10, validators=[validate_integer])

    store_type = models.CharField(max_length=2, choices=StoreType.choices)

    def __str__(self) -> str:
        return self.store_name
    

class HoghoughyStore(Store):
    name_CEO = models.CharField(max_length=255)
    registration_date = models.DateField()
    registration_num = models.CharField(max_length=255)
    national_id = models.CharField(max_length=255, verbose_name='شناسه (کد) ملی')
    economic_code = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.store_name
    

class HaghighyStore(Store):
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    national_code = models.CharField(max_length=15, validators=[validate_integer])
    shomaare_shenasnaame = models.CharField(max_length=15, validators=[validate_integer])

    def __str__(self) -> str:
        return self.store_name


class ProductProperties(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    properties = models.ManyToManyField(ProductProperties, related_name='categories')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='store/product-category-images/')

    def __str__(self) -> str:
        return self.name
    

class ProductSubCategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='store/product-subcategory-images/')

    def __str__(self) -> str:
        return self.name
    

class BaseProduct(models.Model):

    class ProductAuthenticity(models.TextChoices):
        ORIGINAL = 'org', _('اورجینال')
        HIGH_COPY = 'hc', 'های کپی'
        COPY = 'c', 'کپی'
    
    class ProductWarranty(models.TextChoices):
        HAS = 'h', _('دارد')
        DOES_NOT_HAVE = 'dh', _('ندارد')

    class ShipingMethod(models.TextChoices):
        PISHTAAZ = 'pi', _('پیشتاز')

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', null=True)
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, related_name='products', null=True)
    title_farsi = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255)
    product_code = models.CharField(max_length=6, unique=True)
    authenticity = models.CharField(max_length=3, choices=ProductAuthenticity.choices, default=ProductAuthenticity.ORIGINAL)
    warranty = models.CharField(max_length=2, choices=ProductWarranty.choices, default=ProductWarranty.HAS)
    shiping_method = models.CharField(max_length=2, choices=ShipingMethod.choices)

    def __str__(self) -> str:
        return self.title_farsi
    

class SetProductProperty(models.Model):
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='properties')
    property = models.ForeignKey(ProductProperties, on_delete=models.CASCADE)
    value = models.CharField(max_length=250)

    def __str__(self):
        return f'property {self.property} for {self.product.title_farsi} with value {self.value}'
    

class ProductComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='comments')

    text = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user
    

class Product(models.Model):

    class ProductUnit(models.TextChoices):
        PAIR = 'p', _('جفت')

    class ProductStatus(models.TextChoices):
        APPROVED = 'ap', _('تایید شده')
        WAITING = 'w', _('در انتظار تایید')
        NOT_APPROVED = 'na', _('تایید نشده')

    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='products')

    size = models.CharField(max_length=4, choices=ProductSize.choices)
    inventory = models.PositiveIntegerField()
    slug = models.SlugField(null=True)
    unit = models.CharField(max_length=1, choices=ProductUnit.choices)
    unit_price = models.IntegerField()

    discount_percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=True, blank=True)
    start_discount_datetime = models.DateTimeField(null=True, blank=True)
    end_discount_datetime = models.DateTimeField(null=True, blank=True)

    length_package = models.IntegerField(null=True, blank=True)
    width_package = models.IntegerField(null=True, blank=True)
    height_package = models.IntegerField(null=True, blank=True)
    weight_package = models.IntegerField(null=True, blank=True)

    shenaase_kaala = models.CharField(max_length=25)
    barcode = models.CharField(max_length=25)

    product_status = models.CharField(max_length=2, choices=ProductStatus.choices, default=ProductStatus.WAITING)
    active_status = models.BooleanField(default=False)

    reason = models.TextField(
        null=True,
        blank=True,
        help_text=_('به هنگام  خارج کردن وضعیت محصول از در انتظار تایید این بخش پر شود')
    )

    def save(self, *args, **kwargs):
        self.slug = self.generate_unique_slug(self.pk, self.shenaase_kaala, self.barcode)
        return super().save(*args, **kwargs)
    
    def generate_unique_slug(self, value1, value2, value3):
        return f'{value1}--{value2}--{value3}'
    
    def __str__(self) -> str:
        return self.base_product.title_farsi


class ProductImage(models.Model):
    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/product-images/')
    is_cover = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.base_product.title_farsi


class ShipingRange(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    

class ShipingMethod(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class ShipingProperty(models.Model):
    # store: must be one to one field
    shiping_range = models.ManyToManyField(ShipingRange, related_name='shiping_property')
    shiping_method = models.ManyToManyField(ShipingMethod, related_name='shiping_method')


class ShipingCost(models.Model):
    shiping_method = models.ForeignKey(ShipingMethod, on_delete=models.CASCADE, related_name='shiping_cost')
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    cost = models.IntegerField()


class ContactUs(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_num = models.CharField(max_length=11, validators=[validate_integer])
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return f'{self.full_name}: {self.email}'
