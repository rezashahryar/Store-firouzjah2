# Generated by Django 5.1.2 on 2024-10-18 18:04

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_alter_shipingproperty_shiping_method_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ReplyComment',
            new_name='ProductReplyComment',
        ),
    ]
