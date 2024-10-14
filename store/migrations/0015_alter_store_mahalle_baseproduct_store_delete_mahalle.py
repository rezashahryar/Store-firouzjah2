# Generated by Django 5.1.2 on 2024-10-14 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_city_store_mahalle_mantaghe_province_haghighystore_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='mahalle',
            field=models.CharField(max_length=255),
        ),
        migrations.AddField(
            model_name='baseproduct',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='store.store'),
        ),
        migrations.DeleteModel(
            name='Mahalle',
        ),
    ]