# Generated by Django 5.1.2 on 2024-10-14 22:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0015_alter_store_mahalle_baseproduct_store_delete_mahalle'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestPhotographyService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('mobile_num', models.CharField(max_length=11, validators=[django.core.validators.validate_integer])),
                ('address', models.TextField()),
                ('store_name', models.CharField(max_length=255)),
                ('request_text', models.TextField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_photography', to='store.city')),
                ('mantaghe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_photography', to='store.mantaghe')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_photography', to='store.province')),
            ],
        ),
    ]
