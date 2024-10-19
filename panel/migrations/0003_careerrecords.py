# Generated by Django 5.1.2 on 2024-10-19 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareerRecords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('job_position', models.CharField(max_length=255, verbose_name='پست سازمانی')),
                ('reason_leaving_work', models.TextField()),
                ('duration_activity_based_month', models.IntegerField()),
                ('insurance_period_based_month', models.IntegerField()),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='career_records', to='panel.staff')),
            ],
        ),
    ]