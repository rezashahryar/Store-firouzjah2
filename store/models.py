from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from .model_fields import ProductSize
# Create your models here.


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

    # store
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products', null=True)
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

    shenaase_kaala = models.CharField(max_length=25, null=True, blank=True)
    barcode = models.CharField(max_length=25, null=True, blank=True)

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
