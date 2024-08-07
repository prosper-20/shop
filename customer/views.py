from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.urls import reverse
from .forms import CustomerForm, EditCustomerForm, ApproverEditCustomerForm, ReviwerEditCustomerForm
from collections import Counter    
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import datetime
import csv

def is_admin(user):
    return user.is_superuser or user.is_staff

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



# @login_required

# THIS IS FOR THE REVIEW OFFICER
@user_passes_test(is_admin)
def update_customer_form(request, customer_no):
    customer = get_object_or_404(Customer, no=customer_no)
    if request.method == "GET":
        form = ReviwerEditCustomerForm(instance=customer)
    else:
        form = ReviwerEditCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Account Updated Successfully")
            return redirect(reverse("customer"))
    return render(request, "customer/customer_admin_update_customer_form.html", {"form": form})



# THIS IS FOR THE APPROVAL OFFICER OFFICER
@user_passes_test(is_admin)
def admin_update_customer_form(request, customer_no):
    customer = get_object_or_404(Customer, no=customer_no)
    if request.method == "GET":
        form = ApproverEditCustomerForm(instance=customer)
    else:
        form = ApproverEditCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Account Updated Successfully")
            return redirect(reverse("customer"))
    return render(request, "customer/approver_customer_admin_update_customer_form.html", {"form": form})





@user_passes_test(is_admin)
def admin_customer_pdf(request):
    pending_customers = Customer.objects.filter(approval=False)
    customer_count = pending_customers.count()
    html = render_to_string('customer/customer_pdf.html', {'pending_customers': pending_customers, "customer_count": customer_count})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=customer_data.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response



@user_passes_test(is_admin)
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
    field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            
            data_row.append(value)
        writer.writerow(data_row)
    return response
    export_to_csv.short_description = 'Export to CSV'