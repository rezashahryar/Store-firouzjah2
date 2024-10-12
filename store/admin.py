from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.ShipingRange)
class ShipingRangeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ShipingMethod)
class ShipingMethodAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ShipingProperty)
class ShipingPropertyAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ShipingCost)
class ShipingCostAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.BaseProduct)
class BaseProductAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ['slug']


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['base_product', 'is_cover']
