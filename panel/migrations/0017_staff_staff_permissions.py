# Generated by Django 5.1.2 on 2024-10-27 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('panel', '0016_staff_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='staff_permissions',
            field=models.ManyToManyField(null=True, related_name='staff_set', to='auth.permission'),
        ),
    ]