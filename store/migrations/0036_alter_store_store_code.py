# Generated by Django 5.1.2 on 2024-10-23 20:56

import store.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_alter_order_tracking_code_alter_product_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='store_code',
            field=models.CharField(default=store.models.generate_store_code, max_length=10, unique=True),
        ),
    ]
