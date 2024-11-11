# Generated by Django 5.1.2 on 2024-11-01 14:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('panel', '0001_initial'),
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='feeforsellingproduct',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='store.productcategory'),
        ),
        migrations.AddField(
            model_name='feeforsellingproduct',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='store.producttype'),
        ),
        migrations.AddField(
            model_name='feeforsellingproduct',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selling_fees', to='store.store'),
        ),
        migrations.AddField(
            model_name='feeforsellingproduct',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='store.productsubcategory'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.productcategory'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.producttype'),
        ),
        migrations.AddField(
            model_name='productitem',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.productsubcategory'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requestphotographyservice',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_photography', to='store.city'),
        ),
        migrations.AddField(
            model_name='requestphotographyservice',
            name='mantaghe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_photography', to='store.mantaghe'),
        ),
        migrations.AddField(
            model_name='requestphotographyservice',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_photography', to='store.province'),
        ),
        migrations.AddField(
            model_name='setproductitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='panel.productitem'),
        ),
        migrations.AddField(
            model_name='setproductitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.product'),
        ),
        migrations.AddField(
            model_name='staff',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to='store.city'),
        ),
        migrations.AddField(
            model_name='staff',
            name='mantaghe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to='store.mantaghe'),
        ),
        migrations.AddField(
            model_name='staff',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to='store.province'),
        ),
        migrations.AddField(
            model_name='staff',
            name='reviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='staff',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pages', to='panel.staff'),
        ),
        migrations.AddField(
            model_name='feeforsellingproduct',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selling_fees', to='panel.staff'),
        ),
        migrations.AddField(
            model_name='commonquestion',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='common_questions', to='panel.staff'),
        ),
        migrations.AddField(
            model_name='careerrecords',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='career_records', to='panel.staff'),
        ),
    ]
