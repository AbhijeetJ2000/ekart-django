from django.db import models
from accounts.models import Account

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)  # Optional field
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        if self.address_line_2 is not None:
            return f'{self.address_line_1}, {self.address_line_2}'
        return f'{self.address_line_1}'

    def __str__(self):
        return self.first_name

class Order(models.Model):
    STATUS = [
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=255)
    total = models.FloatField()
    shipping_charge = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





