# Generated by Django 4.2.5 on 2023-09-24 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('paypal', 'PayPal'), ('cash_on_delivery', 'Cash on Delivery')], default='cash_on_delivery', max_length=255),
        ),
    ]