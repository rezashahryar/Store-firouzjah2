# Generated by Django 5.1.2 on 2024-10-14 21:45

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_product_barcode_alter_product_shenaase_kaala'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('shabaa_num', models.CharField(max_length=55)),
                ('mobile_num', models.CharField(max_length=12, validators=[django.core.validators.validate_integer])),
                ('phone_num', models.CharField(max_length=12, validators=[django.core.validators.validate_integer])),
                ('address', models.TextField()),
                ('post_code', models.CharField(max_length=10, validators=[django.core.validators.validate_integer])),
                ('store_type', models.CharField(choices=[('ha', 'حقیقی'), ('ho', 'حقوقی')], max_length=2)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.city')),
            ],
        ),
        migrations.CreateModel(
            name='Mahalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Mantaghe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='HaghighyStore',
            fields=[
                ('store_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.store')),
                ('full_name', models.CharField(max_length=255)),
                ('father_name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('national_code', models.CharField(max_length=15, validators=[django.core.validators.validate_integer])),
                ('shomaare_shenasnaame', models.CharField(max_length=15, validators=[django.core.validators.validate_integer])),
            ],
            bases=('store.store',),
        ),
        migrations.CreateModel(
            name='HoghoughyStore',
            fields=[
                ('store_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.store')),
                ('name_CEO', models.CharField(max_length=255)),
                ('registration_date', models.DateField()),
                ('registration_num', models.CharField(max_length=255)),
                ('national_id', models.CharField(max_length=255, verbose_name='شناسه (کد) ملی')),
                ('economic_code', models.CharField(max_length=255)),
            ],
            bases=('store.store',),
        ),
        migrations.AddField(
            model_name='store',
            name='mahalle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.mahalle'),
        ),
        migrations.AddField(
            model_name='store',
            name='mantaghe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.mantaghe'),
        ),
        migrations.AddField(
            model_name='store',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='store.province'),
        ),
    ]
