# Generated by Django 4.2.5 on 2023-10-14 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_cart_created_at_cart_updated_at_cartitem_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variations',
        ),
    ]