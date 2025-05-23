from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.urls import reverse
from .forms import (
    CustomerForm,
    EditCustomerForm,
    ApproverEditCustomerForm,
    ReviwerEditCustomerForm,
)
from collections import Counter
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import datetime
import csv
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.db.models import Q


def is_admin(user):
    return user.is_superuser or user.is_staff


# Create your views here.
@login_required
def customer(request):
    count = Customer.objects.exclude(status="exited").count()
    search_query = request.GET.get("search", "")
    customer_list = Customer.objects.all().order_by("no")

    if search_query:
        customer_list = customer_list.filter(
            Q(name__icontains=search_query)
            | Q(business__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(no__icontains=search_query)
        )

    paginator = Paginator(customer_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    nature_counts = Counter(Customer.objects.values_list("nature", flat=True))
    labels = list(nature_counts.keys())
    data = list(nature_counts.values())

    return render(
        request,
        "customer/customer.html",
        {
            "count": count,
            "page_obj": page_obj,
            "labels": labels,
            "data": data,
            "search_query": search_query,
        },
    )


@login_required
def customer_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = CustomerForm()
        else:
            customer = Customer.objects.get(pk=id)
            form = CustomerForm(instance=customer)
        return render(request, "customer/customer_form.html", {"form": form})
    else:
        if id == 0:
            form = CustomerForm(request.POST)
        else:
            customer = Customer.objects.get(pk=id)
            form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
        return redirect("customer")


@login_required
def new_customer_form(request):
    if request.method == "GET":
        form = CustomerForm()
    else:
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer Account  Creation Successful")
            return redirect("customer")
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
            customer.is_reviewed = True
            customer.save()
            messages.success(request, "Customer Account Updated Successfully")
            return redirect(reverse("customer"))
    return render(
        request, "customer/customer_admin_update_customer_form.html", {"form": form}
    )


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
            customer.approval = True
            customer.save()
            messages.success(request, "Customer Account Updated Successfully")
            return redirect(reverse("customer"))
    return render(
        request,
        "customer/approver_customer_admin_update_customer_form.html",
        {"form": form},
    )


@user_passes_test(is_admin)
def admin_customer_pdf(request):
    pending_customers = Customer.objects.filter(approval=False)
    customer_count = pending_customers.count()
    html = render_to_string(
        "customer/customer_pdf.html",
        {"pending_customers": pending_customers, "customer_count": customer_count},
    )
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename=customer_data.pdf"
    weasyprint.HTML(string=html).write_pdf(response)
    return response


@user_passes_test(is_admin)
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename={opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")

            data_row.append(value)
        writer.writerow(data_row)
    return response
    export_to_csv.short_description = "Export to CSV"


import pandas as pd


def upload_customers(request):
    if request.method == "GET":
        # Get the uploaded file
        excel_file = "C:/Users/edwar/Documents/PROJECTS/KLINSMAN_BROTHER/MyProject/customer/customer_data.xlsx"

        # Read the spreadsheet
        try:
            df = pd.read_excel(excel_file)
            print(df.head())
            print(df.shape)
        except Exception as e:
            return HttpResponse({"error": f"Error reading file: {str(e)}"})

        # Iterate through rows and create customers
        customers_created = 0
        errors = []
        for index, row in df.iterrows():
            try:
                # Extract fields from the row (update based on your spreadsheet column names)
                no = str(row["Customer ID/no"])
                # title = 'Mr'
                name = row["name"]
                business = row["business"]
                email = row["email"]
                phone = str(row["phone"])
                dob = parse_date(str(row["date_of_birth"]))
                address = row["Customer address"]
                state = row["Customer state", "Lagos"]
                other_state = row.get("other_state", None)
                occupation = row["Customer occupation"]
                nature = row["naturebusiness of "]
                status = row.get("status", "new")
                is_reviewed = row.get("is_reviewed", "Not Reviewed")
                date = parse_date(str(row["date"]))
                outstanding_balance = row.get("outstanding_balance", 0)
                data_entry_officer_note = row.get("data_entry_officer_note", "")
                review_officer_note = row.get("review_officer_note", "")
                approval_officer_note = row.get("approval_officer_note", "")
                approval = bool(row.get("approval", False))
                exitdate = parse_date(str(row.get("exitdate", None)))
                nextdue = parse_date(str(row.get("nextdue", None)))

                # Create a Customer instance
                customer = Customer(
                    no=no,
                    title="Mr",
                    name=name,
                    business=business,
                    email=email,
                    phone=phone,
                    dob=dob,
                    address=address,
                    state=state,
                    other_state=other_state,
                    occupation=occupation,
                    nature=nature,
                    status=status,
                    is_reviewed=is_reviewed,
                    date=date,
                    outstanding_balance=outstanding_balance,
                    data_entry_officer_note=data_entry_officer_note,
                    review_officer_note=review_officer_note,
                    approval_officer_note=approval_officer_note,
                    approval=approval,
                    exitdate=exitdate,
                    nextdue=nextdue,
                )
                customer.save()
                customers_created += 1
            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")

        return HttpResponse(f"success: {customers_created} customers created.")

    return render(request, "web/home.html")
