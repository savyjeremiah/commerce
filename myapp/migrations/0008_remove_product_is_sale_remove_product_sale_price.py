# Generated by Django 5.1.4 on 2024-12-21 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_product_is_sale_product_sale_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_sale',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sale_price',
        ),
    ]
