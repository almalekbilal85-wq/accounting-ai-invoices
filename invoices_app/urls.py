from django.urls import path
from invoices_app import views

app_name = 'invoices_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
]
