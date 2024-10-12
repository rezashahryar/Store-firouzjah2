from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from .model_fields import ProductSize
# Create your models here.


class ProductCategory(models.Model):
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
    title_farsi = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255)
    product_code = models.CharField(max_length=6, unique=True)
    authenticity = models.CharField(max_length=3, choices=ProductAuthenticity.choices, default=ProductAuthenticity.ORIGINAL)
    warranty = models.CharField(max_length=2, choices=ProductWarranty.choices, default=ProductWarranty.HAS)
    shiping_method = models.CharField(max_length=2, choices=ShipingMethod.choices)

    def __str__(self) -> str:
        return self.title_farsi
    

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
    unit = models.CharField(max_length=1, choices=ProductUnit.choices)
    unit_price = models.IntegerField()

    discount_percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    start_discount_datetime = models.DateTimeField()
    end_discount_datetime = models.DateTimeField()

    length_package = models.IntegerField()
    width_package = models.IntegerField()
    height_package = models.IntegerField()
    weight_package = models.IntegerField()

    shenaase_kaala = models.CharField(max_length=25)
    barcode = models.CharField(max_length=25)

    product_status = models.CharField(max_length=2, choices=ProductStatus.choices, default=ProductStatus.WAITING)
    active_status = models.BooleanField(default=False)


class ProductImage(models.Model):
    base_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=f'store/product-{base_product}/')
    is_cover = models.BooleanField(default=False)


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
