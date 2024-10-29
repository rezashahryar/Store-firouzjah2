# Generated by Django 5.1.2 on 2024-10-24 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0009_contract'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staff',
            options={'permissions': [('slider_settings', 'slider settings'), ('contract_settings', 'contract settings'), ('list_of_staffs', 'list of staffs'), ('list_of_users', 'list of users'), ('list_of_products (approved)', 'list of products (approved)'), ('list_of_products (waiting)', 'list of products (waiting)'), ('list_of_all_products', 'list of all products'), ('list_of_products (not_approved)', 'list of products (not approved)'), ('create_new_product', 'create new product'), ('list_of_stores (waiting)', 'list of stores (waiting)'), ('list_of_stores (approved)', 'list of stores (approved)'), ('list_of_stores (not_approved)', 'list of stores (not approved)'), ('support_of_stores', 'support of stores'), ('orders (delivered)', 'orders (delivered)'), ('list_of_customers', 'list of customers'), ('add_category', 'add category'), ('add_item', 'add item'), ('request_photography_service', 'request photography service'), ('backup', 'backup'), ('index_page', 'index page'), ('banner_settings', 'banner settings'), ('registration_of_staff', 'registration of staff'), ('request_staff', 'request staff'), ('contact_us', 'contact us'), ('list_of_all_stores', 'list of all stores'), ('list_of_all_orders', 'list of all orders'), ('list_of_return_orders', 'list of return orders'), ('list_of_current_orders', 'list of current orders'), ('list_of_canceled_orders', 'list of canceled orders'), ('all_categories', 'all categories'), ('add_product_type', 'add product type'), ('pages_settings', 'pages settings'), ('support_customers', 'support customers'), ('support_staffs', 'support staffs'), ('add_sub_category', 'add sub category'), ('transactions', 'transactions'), ('common_questions', 'common questions'), ('web_mail', 'web mail'), ('public_settings', 'public settings'), ('product_box_settings', 'product_box_settings'), ('edit_profile', 'edit profile')]},
        ),
    ]
