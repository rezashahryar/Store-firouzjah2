# Generated by Django 5.1.2 on 2024-10-12 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_baseproduct_category_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
