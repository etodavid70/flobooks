from django.db import models
from sales.models import Sale

# class VAT(models.Model):
#     sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
#     vat_rate = models.FloatField( default=7.5)  # 7.5%
#     vat_amount = models.FloatField( default=0.00)

#     def __str__(self):
#         return f"VAT for Sale {self.sale.id}"


# class VATTracker(models.Model):
#     total_vat = models.FloatField( default=0.00)

#     def __str__(self):
#         return f"Total VAT Collected: {self.total_vat}"

# Create your models here.



# class VAT(models.Model):
#     total_vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def add_vat(self, vat_amount):
#         self.total_vat += vat_amount
#         self.save()



from decimal import Decimal


# class VAT(models.Model):
#     total_vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     commencement_date = models.DateTimeField(default=timezone.now)  # User sets this date
#     vat_due = models.BooleanField(default=False)  # Tracks if VAT is due

#     def add_vat(self, vat_amount):
#         self.total_vat += vat_amount
#         self.save()

#     def is_vat_due(self):
#         # Calculate if one month has passed since the commencement date
#         one_month_after_commencement = self.commencement_date + timedelta(days=30)
#         if datetime.now() >= one_month_after_commencement:
#             # VAT is due if total VAT is not zero for the month
#             self.vat_due = self.total_vat > 0
#         else:
#             self.vat_due = False
#         self.save()
#         return self.vat_due

from datetime import timedelta
from django.utils import timezone

class VAT(models.Model):
    total_vat = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    commencement_date = models.DateTimeField(default=timezone.now)  # Default to current date
    vat_due = models.BooleanField(default=False)

    def add_vat(self, vat_amount):
        self.total_vat += vat_amount
        self.save()

    def is_vat_due(self):
        one_month_after_commencement = self.commencement_date + timedelta(days=30)

        # Ensure both are aware datetime objects
        if timezone.now() >= one_month_after_commencement:
            self.vat_due = self.total_vat > 0
        else:
            self.vat_due = False

        self.save()
        return self.vat_due



