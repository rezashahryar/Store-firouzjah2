from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from . import models

# Register your models here.


@admin.register(models.ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    ...


@admin.register(models.SimilarProduct)
class SimilarProductAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product__base_product')


@admin.register(models.ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    ...


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Mantaghe)
class MantagheAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'user', 'store_code', 'store_type']


@admin.register(models.HoghoughyStore)
class HoghoughyStore(admin.ModelAdmin):
    ...


@admin.register(models.HaghighyStore)
class HaghighyStoreAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ShipingRange)
class ShipingRangeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ShipingMethod)
class ShipingMethodAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ShipingProperty)
class ShipingPropertyAdmin(admin.ModelAdmin):
    list_display = ['store']


@admin.register(models.ShipingCost)
class ShipingCostAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


@admin.register(models.ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


@admin.register(models.ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):
    ...


@admin.register(models.BaseProduct)
class BaseProductAdmin(admin.ModelAdmin):
    list_display = ['title_farsi', 'store', 'category', 'sub_category', 'product_type']


@admin.register(models.ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'unit_price', 'inventory', 'unit_price', 'discount_percent', 'shenaase_kaala', 'barcode',
        'product_status', 'active_status'
    ]
    list_editable = ['discount_percent', 'product_status', 'active_status']
    readonly_fields = ['slug']
    list_select_related = ['base_product']

    @admin.display(ordering='base_product__title_farsi')
    def title(self, obj):
        return obj.base_product.title_farsi


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['base_product', 'is_cover']


@admin.register(models.ProductProperties)
class ProductPropertiesAdmin(admin.ModelAdmin):
    ...


@admin.register(models.SetProductProperty)
class SetProductPropertyAdmin(admin.ModelAdmin):
    ...


class CartItemInline(admin.TabularInline):
    model = models.CartItem
    fields = ['product', 'quantity']
    extra = 1


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ReportProduct)
class ReportProductAdmin(admin.ModelAdmin):
    ...


class OrderItemTabularInline(admin.TabularInline):
    model = models.OrderItem
    fields = ['product' ,'purchased_price' ,'quantity']
    extra = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['email', 'status']
    list_editable = ['status']
    inlines = [OrderItemTabularInline]

    def email(self, obj):
        return obj.customer.user.email


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    ...


class OrderCustomerInline(admin.TabularInline):
    model = models.Order
    fields = ['full_name_recipient', 'mobile_recipient', 'tracking_code', 'status']
    extra = 1


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']
    inlines = [OrderCustomerInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related('user')
