# Generated by Django 5.1.2 on 2024-10-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_producttype_baseproduct_product_type_similarproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='store_code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
