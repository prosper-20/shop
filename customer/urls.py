from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer, name="customer"),
    path('form/', views.new_customer_form, name="customer_form"), # you changed this to new_customer_form
    path('customer/<int:id>', views.customer_form, name="customer_update"),
 
]

