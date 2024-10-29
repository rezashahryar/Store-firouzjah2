# Generated by Django 5.1.2 on 2024-10-28 14:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0019_alter_staff_adame_sooe_pishine_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='datetime_modified',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
    ]