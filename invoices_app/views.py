from django.shortcuts import render
from .forms import UploadFileForm
from File_processing.api_connection import getAIOutput
import json
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
