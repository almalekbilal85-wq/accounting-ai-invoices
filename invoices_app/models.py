from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=256)
    org_number = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, related_name='invoices', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=256)
    invoice_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3,default="SEK")
    created_at = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=256)
    description = models.TextField()

    file = models.FileField(
        upload_to="invoices/"
    )

    def __str__(self):
        return self.invoice_number
    


class AccountingLine(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='accounting_lines',  on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10)
    debit = models.DecimalField(max_digits=12, decimal_places=2)
    credit = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.account_number