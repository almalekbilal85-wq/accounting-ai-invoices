from django.contrib import admin
from invoices_app.models import Customer, Invoice, AccountingLine
# Register your models here.

admin.site.register(Customer)
admin.site.register(Invoice)
admin.site.register(AccountingLine)
