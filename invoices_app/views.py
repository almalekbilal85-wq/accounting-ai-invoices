from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm, JournalForm, AccountingLineForm, InvoiceForm, AccountingLineFormSet
from File_processing.api_connection import getAIOutput
import json

from django.views.generic import View, ListView, DetailView, CreateView, DeleteView, UpdateView
from invoices_app import models
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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


@login_required
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

@login_required
def edit_journal(request, journal_id):
    journal = get_object_or_404(models.Journal, id=journal_id)
    customer = journal.customer

    # Get first invoice if it exists
    invoice = journal.invoices.first()

    if request.method == "POST":
        journal_form = JournalForm(
            request.POST,
            instance=journal
        )

        formset = AccountingLineFormSet(
            request.POST,
            instance=journal
        )

        invoice_form = InvoiceForm(
            request.POST,
            request.FILES,
            instance=invoice
        )

        if journal_form.is_valid() and formset.is_valid():

            journal = journal_form.save()

            formset.instance = journal
            formset.save()

            # Invoice handling
            if journal.type == "invoice" and invoice_form.is_valid():
                invoice = invoice_form.save(commit=False)
                invoice.journal = journal
                invoice.save()

            # Optional: delete invoice if type changed away from invoice
            elif journal.type != "invoice":
                journal.invoices.all().delete()

            return redirect(
                "invoices_app:customer_detail",
                pk=customer.id
            )

    else:
        journal_form = JournalForm(instance=journal)

        formset = AccountingLineFormSet(
            instance=journal
        )

        invoice_form = InvoiceForm(
            instance=invoice
        )

    return render(
        request,
        "invoices_app/journal_form.html",
        {
            "journal_form": journal_form,
            "formset": formset,
            "invoice_form": invoice_form,
            "customer": customer,
            "journal": journal,
        },
    )

##########################################

class CustomerListView(LoginRequiredMixin,ListView):
    login_url = 'login'
    redirect_field_name = '/'

    model = models.Customer

class CustomerDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = '/'

    model = models.Customer
    template_name = 'invoices_app/customer_detail.html'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = '/'

    fields = ('name', 'org_number', 'address')
    model = models.Customer

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    redirect_field_name = '/'

    fields = ('name', 'org_number', 'address')
    model = models.Customer

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = '/'

    model = models.Customer
    success_url = reverse_lazy('invoices_app:customers_list')


class JournalDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    redirect_field_name = '/'

    model = models.Journal
    template_name = 'invoices_app/journal_detail.html'

class JournalDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = '/'
    
    model = models.Journal
    success_url = reverse_lazy('invoices_app:customers_list')
###########################

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def attach_account_descriptions(ai_result: dict) -> dict:
    """
    Takes AI JSON result and adds account descriptions
    to each accounting entry.
    """

    entries = ai_result.get("accounting_entries", [])

    for entry in entries:
        account_number = entry.get("account")

        if account_number:
            try:
                account = models.Account.objects.get(account_number=account_number)
                entry["description"] = account.description
            except models.Account.DoesNotExist:
                entry["description"] = None

    return ai_result

@login_required
@csrf_exempt
def ai_journal_extract(request):

    if request.method == "POST":

        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        extension = uploaded_file.name.split(".")[-1].lower()

        result = json.loads(getAIOutput(uploaded_file, extension))

        result = attach_account_descriptions(result)

        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request"}, status=400)



@login_required
def account_lookup(request):
    """
    Examples:

    /api/account-lookup/?account_number=1900

    /api/account-lookup/?description=Kassa
    """

    account_number = request.GET.get("account_number")
    description = request.GET.get("description")

    try:
        if account_number:
            account = models.Account.objects.get(account_number=account_number)

        elif description:
            account = models.Account.objects.get(description__iexact=description)

        else:
            return JsonResponse(
                {"error": "account_number or description is required"},
                status=400
            )

        return JsonResponse({
            "account_number": account.account_number,
            "description": account.description,
        })

    except models.Account.DoesNotExist:
        return JsonResponse(
            {"error": "Account not found"},
            status=404
        )