# Generated by Django 5.1.2 on 2024-10-15 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_reportproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipingproperty',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shiping_properties', to='store.store'),
        ),
    ]
