# Generated by Django 5.1.4 on 2024-12-21 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_product_sale_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sale_price',
        ),
    ]
