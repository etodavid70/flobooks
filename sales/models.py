from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from onboarding.models import CustomUser

class Customer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="customer")
    name = models.CharField(max_length=255)
    phoneNumber=models.CharField(max_length=11, default="")
    address= models.CharField(max_length=255, default="")

    def __str__(self):
        return self.name

class Item(models.Model):
    date_registered = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="item")  # Add this line
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_item_name_per_user')
        ]


class Sale(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='sales')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    STATUS_CHOICES = (
        ('Paid', 'P'),
        ('Credit', 'C'),
    )
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='Paid')

    def __str__(self):
        return f"{self.customer.name} - {self.item.name} - {self.date}"



class Purchase(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # customer = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='purchase')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    dealers_name=models.CharField(default="", max_length= 120)
    STATUS_CHOICES = (
        ('Paid', 'P'),
        ('Credit', 'C'),
    )
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='Paid')

    def __str__(self):
        return f"{self.customer.name} - {self.item.name} - {self.date}"




class Invoice(models.Model):
    sales = models.ManyToManyField(Sale)  # Allow multiple sales per invoice
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=6, choices=Sale.STATUS_CHOICES)

    def __str__(self):
        return f"Invoice for {self.sales.first().customer} on {self.date}"  # Assuming all sales have the same customer


class Accounts(models.Model):

    sales_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    cash_account = models.JSONField()
    bank_account = models.JSONField()

    def __str__(self):
        return self.sales_id

class AccountsPurchase(models.Model):

    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    cash_account = models.JSONField()
    bank_account = models.JSONField()

    def __str__(self):
        return self.purchase_id



from django.db import models
from django.conf import settings
from django.utils import timezone

class AccountsReceivable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts_receivable')
    amount = models.DecimalField(max_digits=10, decimal_places=2)




    def __str__(self):
        return f'{self.customer_name} owes {self.amount_due}'

    def is_due(self):
        """Returns whether the account is due for payment"""
        return self.due_date <= timezone.now()


