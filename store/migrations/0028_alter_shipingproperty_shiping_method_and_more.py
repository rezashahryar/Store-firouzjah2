# Generated by Django 5.1.2 on 2024-10-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_alter_shipingproperty_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipingproperty',
            name='shiping_method',
            field=models.ManyToManyField(related_name='Shiping_method', to='store.shipingmethod'),
        ),
        migrations.AlterField(
            model_name='shipingproperty',
            name='shiping_range',
            field=models.ManyToManyField(related_name='Shiping_property', to='store.shipingrange'),
        ),
    ]
