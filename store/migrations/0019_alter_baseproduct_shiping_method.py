# Generated by Django 5.1.2 on 2024-10-15 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_productcomment_replycomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseproduct',
            name='shiping_method',
            field=models.CharField(choices=[('pi', 'پیشتاز'), ('ti', 'تیپاکس'), ('ba', 'باربری'), ('mo', 'پیک موتوری')], max_length=2),
        ),
    ]