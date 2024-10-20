from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(models.RequestPhotographyService)
class RequestPhotographyServiceAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    ...


@admin.register(models.CareerRecords)
class CareerRecordsAdmin(admin.ModelAdmin):
    ...
