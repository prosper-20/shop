from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.urls import reverse
from .forms import CustomerForm, EditCustomerForm
from collections import Counter    
from django.contrib import messages


# Create your views here.
@login_required
def customer (request):
    count = Customer.objects.exclude(status='exited').count()
    customers = Customer.objects.all()
    nature_counts = Counter(customers.values_list('nature', flat=True))
    labels = list(nature_counts.keys())
    data = list(nature_counts.values())

    
    return render(request, 'customer/customer.html', {'count': count, 'customer_list' : Customer.objects.all(), 'labels': labels, 'data': data})

@login_required
def customer_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = CustomerForm()
        else:
            customer = Customer.objects.get(pk=id)
            form = CustomerForm(instance=customer)
        return render(request, 'customer/customer_form.html', {'form':form})
    else:
        if id == 0:
            form = CustomerForm(request.POST)
        else:
            customer = Customer.objects.get(pk=id)
            form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('customer')
    

@login_required
def new_customer_form(request):
    if request.method == "GET":
        form = CustomerForm()
    else:
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Account Successful")
            return redirect('customer')
    return render(request, "customer/customer_form.html", {"form": form})



@login_required
def update_customer_form(request, customer_no):
    customer = get_object_or_404(Customer, no=customer_no)
    if request.method == "GET":
        form = EditCustomerForm(instance=customer)
    else:
        form = EditCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Account Updated Successfully")
            return redirect(reverse("customer"))
    return render(request, "customer/customer_admin_update_customer_form.html", {"form": form})