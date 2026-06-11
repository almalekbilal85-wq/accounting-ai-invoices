from django.contrib import admin
from invoices_app.models import Customer, Invoice, AccountingLine, Journal, Account
# Register your models here.

admin.site.register(Customer)
admin.site.register(Journal)
admin.site.register(Invoice)
admin.site.register(AccountingLine)
admin.site.register(Account)
