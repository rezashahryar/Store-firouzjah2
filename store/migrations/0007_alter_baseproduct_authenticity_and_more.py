# Generated by Django 5.1.2 on 2024-11-07 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_baseproduct_product_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseproduct',
            name='authenticity',
            field=models.CharField(choices=[('org', 'اورجینال'), ('hc', 'های کپی'), ('c', 'کپی')], max_length=3),
        ),
        migrations.AlterField(
            model_name='baseproduct',
            name='warranty',
            field=models.CharField(choices=[('h', 'دارد'), ('dh', 'ندارد')], max_length=2),
        ),
    ]
