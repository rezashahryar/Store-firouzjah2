# Generated by Django 5.1.2 on 2024-10-13 19:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_productproperties_productcategory_properties_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_percent',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='end_discount_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='height_package',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='length_package',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='shenaase_kaala',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='start_discount_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight_package',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='width_package',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]