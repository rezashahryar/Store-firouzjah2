from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from . import models

# Register your models here.


@admin.register(models.Contract)
class ContractAdmin(admin.ModelAdmin):
    ...


@admin.register(models.FeeForSellingProduct)
class FeeForSellingProductAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = 'text'


@admin.register(models.CommonQuestion)
class CommonQuestionAdmin(SummernoteModelAdmin):
    summernote_fields = 'text'


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'user_username', 'mobile']
    list_select_related = ['user']

    def user_email(self, profile):
        if profile.user.email:
            return profile.user.email
        return 'None'
    
    def user_username(self, profile):
        return profile.user.username


@admin.register(models.RequestPhotographyService)
class RequestPhotographyServiceAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'gender', 'mobile_num', 'email', 'birth_date', 'datetime_created', 'status']
    exclude = ['reviewer', 'reason']


@admin.register(models.CareerRecords)
class CareerRecordsAdmin(admin.ModelAdmin):
    ...
