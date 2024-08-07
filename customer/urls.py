from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer, name="customer"),
    path("all/", views.admin_customer_pdf, name="print-all-customers"),
    path('form/', views.new_customer_form, name="customer_form"), # you changed this to new_customer_form
    path('<int:id>', views.customer_form, name="customer_update"),
    path("update/<int:customer_no>/", views.update_customer_form, name="update-customer-form"),
    path("update/<int:customer_no>/approve/", views.admin_update_customer_form, name="admin-update-customer-form"),

 
]

