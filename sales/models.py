from django.db import models
from django.contrib.auth.models import User

from onboarding.models import CustomUser

class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="customer")
    name = models.CharField(max_length=255)
    phoneNumber=models.CharField(max_length=11, default="")

    def __str__(self):
        return self.name

class Item(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="item")  # Add this line
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Sale(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=5)
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('C', 'Completed'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"{self.customer.name} - {self.item.name} - {self.date}"


class Invoice(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=Sale.STATUS_CHOICES)

    def __str__(self):
        return f"Invoice for {self.sale.customer.name} on {self.date}"

class Accounts(models.Model):

    sales_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    cash_account = models.JSONField()
    bank_account = models.JSONField()

    def __str__(self):
        return self.sales_id

