# Generated by Django 5.1.2 on 2024-10-23 21:01

import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_remove_baseproduct_product_code_product_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(default=store.models.generate_product_code, max_length=6, unique=True),
        ),
    ]
