from decimal import Decimal
import random

from uuid import uuid1, uuid4

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, validate_integer
from django.conf import settings
from django.db import IntegrityError

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
    

def generate_store_code():
    while True:
        try:
            code = random.randint(100000, 999999)
            return code
        except IntegrityError:
            continue


class Store(models.Model):

    class StoreType(models.TextChoices):
        HAGHIGHY = 'ha', _('حقیقی')
        HOGHOUGHY = 'ho', _('حقوقی')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='store', null=True)

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

    store_code = models.CharField(max_length=10, unique=True, default=generate_store_code)
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
    user_creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='made_categories', null=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='store/product-category-images/')

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    

class ProductSubCategory(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=uuid1)
    image = models.ImageField(upload_to='store/product-subcategory-images/')

    def __str__(self) -> str:
        return self.name
    

class ProductType(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='product_types')
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, related_name='product_types')
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title
    

class ProductBrand(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='brands')
    name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)

    def __str__(self):
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
        TIPAAX = 'ti', _('تیپاکس')
        BAARBARI = 'ba', _('باربری')
        PEYK_MOTORY = 'mo', _('پیک موتوری')

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    sub_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE, related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(ProductBrand, on_delete=models.PROTECT, related_name='products', null=True)
    title_farsi = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    authenticity = models.CharField(max_length=3, choices=ProductAuthenticity.choices)
    warranty = models.CharField(max_length=2, choices=ProductWarranty.choices)
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

    class Meta:
        ordering = ('-datetime_created',)

    def __str__(self) -> str:
        return f'{self.user} for {self.product}'
    

class ProductReplyComment(models.Model):
    comment = models.ForeignKey(ProductComment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='replies')

    text = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} for {self.comment.text[:10]}'
    

class ProductColor(models.Model):
    name = models.CharField(max_length=255)
    code_color = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active_status=True, product_status=Product.ProductStatus.APPROVED)

    def available_products(self):
        return self.get_queryset().filter(inventory__gt=0)
    

def generate_product_code():
    while True:
        try:
            code = random.randint(100000, 999999)
            return code
        except IntegrityError:
            continue
    

class Product(models.Model):

    class ProductUnit(models.TextChoices):
        PAIR = 'p', _('جفت')

    class ProductStatus(models.TextChoices):
        APPROVED = 'ap', _('تایید شده')
        WAITING = 'w', _('در انتظار تایید')
        NOT_APPROVED = 'na', _('تایید نشده')

    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='products')
    product_code = models.CharField(max_length=6, unique=True, default=generate_product_code)
    inventory = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, allow_unicode=True)
    unit_price = models.IntegerField()

    discount_percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=True, blank=True)
    start_discount_datetime = models.DateTimeField(null=True, blank=True)
    end_discount_datetime = models.DateTimeField(null=True, blank=True)

    length_package = models.IntegerField()
    width_package = models.IntegerField()
    height_package = models.IntegerField()
    weight_package = models.IntegerField()

    shenaase_kaala = models.CharField(max_length=25)
    barcode = models.CharField(max_length=25)

    product_status = models.CharField(max_length=2, choices=ProductStatus.choices, default=ProductStatus.WAITING)
    active_status = models.BooleanField(default=False)

    reviewer = models.ForeignKey('panel.Staff', on_delete=models.CASCADE, related_name='reviewers', null=True, blank=True)
    reason = models.TextField(
        null=True,
        blank=True,
        help_text=_('به هنگام  خارج کردن وضعیت محصول از در انتظار تایید این بخش پر شود')
    )

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    approved = ProductManager()

    # def save(self, *args, **kwargs):
    #     self.slug = self.generate_unique_slug(self.base_product.pk, self.shenaase_kaala, self.barcode)
    #     return super().save(*args, **kwargs)
    
    def generate_unique_slug(self, value1, value2, value3):
        return f'{value1}--{value2}--{value3}'
    
    def __str__(self) -> str:
        return self.base_product.title_farsi
    
    @property
    def cover(self):
        try:
            return self.base_product.images.get(id=self.pk, is_cover=True)
        except ProductImage.DoesNotExist:
            return None
        
    @property
    def price_after_discount(self):
        if self.discount_percent:
            return self.unit_price - int(((self.discount_percent / Decimal(100)) * self.unit_price))
        return None


class ProductImage(models.Model):
    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/product-images/')
    is_cover = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.base_product.title_farsi
    
    def clean(self):
        if ProductImage.objects.filter(base_product_id=self.base_product.pk, is_cover=True) and self.is_cover:
            raise ValidationError('از قبل موجود است is_cover=True عکس برای این محصول با')
        return super().clean()
    

class ReportProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='reports')
    text = models.TextField()

    datetime_created = models.DateTimeField(auto_now_add=True)
    

class SimilarProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='similar_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='similar_products')

    def __str__(self) -> str:
        return str(self.product.base_product.title_farsi)


class ShipingRange(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
    

class ShipingMethod(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class ShipingProperty(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='shiping_property')
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
    

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = [['cart', 'product']]


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')

    def __str__(self) -> str:
        return str(self.user.username)
    

def generate_order_tracking_code():
    while True:
        try:
            code = random.randint(100000, 999999)
            return code
        except IntegrityError:
            continue


class Order(models.Model):

    class OrderStatusChoices(models.TextChoices):
        CURRENT = 'ou', _('جاری')
        DELIVERED = 'od', _('تحویل داده شده')
        RETURN = 'or', _('مرجوع شده')
        CANCELED = 'oc', _('لغو شده')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    
    full_name_recipient = models.CharField(max_length=255)
    mobile_recipient = models.CharField(max_length=11, validators=[validate_integer])
    email_recipient = models.EmailField()
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='orders')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='orders')
    mantaghe = models.ForeignKey(Mantaghe, on_delete=models.CASCADE, related_name='orders')
    mahalle = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    pelaak = models.CharField(max_length=15)
    vaahed = models.CharField(max_length=3)
    post_code = models.CharField(max_length=10, validators=[validate_integer])
    referrer_code = models.CharField(max_length=255)

    tracking_code = models.CharField(max_length=25, unique=True, default=generate_order_tracking_code)

    status = models.CharField(max_length=2, choices=OrderStatusChoices.choices, default=OrderStatusChoices.CURRENT)

    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'order_id={self.pk}'
    
    def get_total_price(self):
        return sum(item.quantity * item.purchased_price for item in self.items.all())
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    purchased_price = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        unique_together = [['order', 'product']]
