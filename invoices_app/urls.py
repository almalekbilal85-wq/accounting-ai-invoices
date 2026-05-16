from django.urls import path
from invoices_app import views

app_name = 'invoices_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('customers/', views.CustomerListView.as_view(), name='customers_list'),
    path('customers/<int:pk>/',views.CustomerDetailView.as_view(),name='customer_detail'),
    path('customers/create/', views.CustomerCreateView.as_view(),name='create_customer'),
    path('customers/update/<int:pk>/', views.CustomerUpdateView.as_view(),name='update_customer'),
    path('customers/delete/<int:pk>/', views.CustomerDeleteView.as_view(),name='delete_customer'),
]
