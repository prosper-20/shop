from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm
from collections import Counter    

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