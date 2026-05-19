from django.db import models
from django.urls import reverse

from django.db.models import F
from django.db import transaction
# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=256)
    org_number = models.CharField(max_length=256)
    address = models.CharField(max_length=256, blank=True, null=True)
    next_journal_number = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return self.name or "Unnamed Customer"
    
    def get_absolute_url(self):
        return reverse("invoices_app:customer_detail", kwargs={"pk": self.pk})

class Journal(models.Model):
    customer = models.ForeignKey(Customer, related_name='journals', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    journal_number = models.PositiveIntegerField(editable=False, blank=True, null=True)
    vat_code = models.CharField(max_length=10, blank=True)

    TYPE_CHOICES = [
        ("manual", "Manual"),
        ("invoice", "Invoice"),
        ("bank", "Bank transaction"),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="invoice")


    def save(self, *args, **kwargs):
        if self.journal_number is None:
            with transaction.atomic():
                customer = Customer.objects.select_for_update().get(pk=self.customer.pk)
                self.journal_number = customer.next_journal_number
                customer.next_journal_number = F("next_journal_number") + 1
                customer.save()

        super().save(*args, **kwargs)

    def __str__(self):
        jounal_str = self.customer.name + ' &&& V-'
        if self.journal_number is not None:
            jounal_str = jounal_str + str(self.journal_number)

        return jounal_str or "Unnamed Journal"

class Invoice(models.Model):

    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, null=True, blank=True)
    invoice_number = models.CharField(max_length=256, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3,default="SEK", blank=True, null=True)
    supplier = models.CharField(max_length=256, blank=True, null=True)

    file = models.FileField(
        upload_to="invoices/",
        blank=True,
         null=True
    )

    def __str__(self):
        return self.invoice_number or "Unnamed invoice"
    


class AccountingLine(models.Model):
    journal = models.ForeignKey(Journal, related_name='accounting_lines',  on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10)
    debit = models.DecimalField(max_digits=12, decimal_places=2)
    credit = models.DecimalField(max_digits=12, decimal_places=2)
    

    def __str__(self):
        return self.account_number