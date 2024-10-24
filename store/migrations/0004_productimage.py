# Generated by Django 5.1.2 on 2024-10-12 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='store/product-<django.db.models.fields.related.ForeignKey>/')),
                ('is_cover', models.BooleanField(default=False)),
                ('base_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.baseproduct')),
            ],
        ),
    ]
