# Generated by Django 5.1.2 on 2024-10-14 22:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseproduct',
            name='sub_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.productsubcategory'),
        ),
    ]
