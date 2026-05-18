from django import forms
from invoices_app.models import Customer, Invoice, AccountingLine, Journal
from django.forms import inlineformset_factory

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ["type", "description", "entry_date"]

class AccountingLineForm(forms.ModelForm):
    class Meta:
        model = AccountingLine
        fields = ["account_number", "debit", "credit"]

AccountingLineFormSet = inlineformset_factory(
    Journal,
    AccountingLine,
    form=AccountingLineForm,
    extra=3,
    can_delete=True
)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["invoice_number", "invoice_date", "due_date", "total_amount", "vat_amount", "currency", "supplier" , "file"]

class UploadFileForm(forms.Form):
    file = forms.FileField()