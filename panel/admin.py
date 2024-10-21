from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    ...


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
    ...


@admin.register(models.CareerRecords)
class CareerRecordsAdmin(admin.ModelAdmin):
    ...
