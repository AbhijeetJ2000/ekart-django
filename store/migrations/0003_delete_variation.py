# Generated by Django 4.2.5 on 2023-10-14 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_remove_cartitem_variations'),
        ('store', '0002_product_created_date_product_updated_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Variation',
        ),
    ]
