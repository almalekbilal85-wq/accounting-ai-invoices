from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm, JournalForm, AccountingLineForm, InvoiceForm, AccountingLineFormSet
from File_processing.api_connection import getAIOutput
import json

from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView
from invoices_app import models
from django.urls import reverse_lazy


# Create your views here.

def index(request):
    return render(request, 'invoices_app/index.html')


def upload(request):

    file_uploaded = ''
    
    data = None
    form = UploadFileForm()  
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            uploaded_file = form.cleaned_data['file']

            file_name = uploaded_file.name
            extension = file_name.split('.')[-1]

            file_data = getAIOutput(uploaded_file, extension)

            data = json.loads(file_data)
            file_name = uploaded_file.name


            file_uploaded = 'The file is succesfully uploaded ' + file_name
        else:
            print(form.errors)
            
            
    return render (request, 'invoices_app/upload_invoices.html', {'form':form, 'text': file_uploaded, 'data': data})



def create_journal(request, customer_id):
    customer = models.Customer.objects.get(id=customer_id)

    if request.method == "POST":

        journal_form = JournalForm(request.POST)
        formset = AccountingLineFormSet(request.POST)
        invoice_form = InvoiceForm(request.POST, request.FILES)

        if journal_form.is_valid() and formset.is_valid():

            journal = journal_form.save(commit=False)
            journal.customer = customer
            journal.save()

            formset.instance = journal
            formset.save()

            # ONLY SAVE INVOICE IF TYPE IS INVOICE
            if journal.type == "invoice" and invoice_form.is_valid():
                invoice = invoice_form.save(commit=False)
                invoice.journal = journal
                invoice.save()

            return redirect("invoices_app:customer_detail", pk=customer.id)

    else:
        journal_form = JournalForm()
        formset = AccountingLineFormSet()
        invoice_form = InvoiceForm()

    return render(request, "invoices_app/journal_form.html", {
        "journal_form": journal_form,
        "formset": formset,
        "invoice_form": invoice_form,
        "customer": customer,
    })

##########################################

class CustomerListView(ListView):
    model = models.Customer

class CustomerDetailView(DetailView):
    model = models.Customer
    template_name = 'invoices_app/customer_detail.html'

class CustomerCreateView(CreateView):
    fields = ('name', 'org_number', 'address')
    model = models.Customer

class CustomerUpdateView(UpdateView):
    fields = ('name', 'org_number', 'address')
    model = models.Customer

class CustomerDeleteView(DeleteView):
    model = models.Customer
    success_url = reverse_lazy('invoices_app:customers_list')