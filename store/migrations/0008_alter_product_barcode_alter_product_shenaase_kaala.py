# Generated by Django 5.1.2 on 2024-11-11 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_baseproduct_authenticity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='barcode',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='product',
            name='shenaase_kaala',
            field=models.CharField(max_length=25),
        ),
    ]