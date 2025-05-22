from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Rate, Shop, Rent, Income, PaymentSlip
from django.db.models import Count
from .forms import ShopForm, IncomeForm, MyShopForm, PaymentSlipEditForm, PaymentSlipForm, EditMyShopForm, AdminEditMyShopForm, EditMyRentForm, CreateRentForm
from django.core.paginator import Paginator
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from decimal import Decimal
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
import weasyprint

def generate_shops(request):
    file_path = r"C:/Users/edwar/Downloads/DBB_Shops.csv"
    shops_df = pd.read_csv(file_path)
    for _, row in shops_df.iterrows():
        shop_id = row[0]
        floor_level = row[1]
        size = row[2]
        rent = float(row[3].replace(',', ''))

        # Create the Shop instance
        shop = Shop.objects.create(
            name=shop_id,
            type='A',  # Default or inferred type
            price=rent,
            no=shop_id,
            address=f"{floor_level}, {shop_id}",
            floor=floor_level[0],  # Extract the floor identifier
            size=size,
            status='vacant',  # Default status
            is_paid=False,  # Default value
            is_approved=False  # Default value
        )

        # Save the shop instance to the database
        shop.save()
    return HttpResponse("DONE")

def home(request):
    return render(request, 'index.html')

@login_required
def shop (request):
    count = Rate.objects.exclude(status='active').count()
    
    allocated_count = Rate.objects.filter(status='active').count()
    vacant_count = Rate.objects.filter(status='vacant').count()
    shoplist = Rate.objects.all().order_by('no')

    p = Paginator(Rate.objects.all(), 5)
    page = request.GET.get('page')
    shops = p.get_page(page)

    context = {
        'count': count,
        'allocated_count': allocated_count,
        'vacant_count' : vacant_count,
        'shoplist' : shoplist,
        'shops': shops,

    }

    return render(request, 'shop/shop.html', context)


@login_required
def myshops(request):
    all_shops = Shop.objects.all().order_by("no")
    context = {"all_shops": all_shops}
    return render(request, "shop/myshop.html", context)


@login_required
def shop_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = ShopForm()
        else:
            rate = Rate.objects.get(pk=id)
            form = ShopForm(instance=rate)
        return render(request, 'shop/shop_form.html', {'form':form})
    else:
        if id == 0:
            form = ShopForm(request.POST)
        else:
            rate = Rate.objects.get(pk=id)
            form = ShopForm(request.POST, instance=rate)
        if form.is_valid():
            form.save()
        return redirect('shop')
    

@login_required
def shop_detail(request, shop_no):
    shop = get_object_or_404(Shop, no=shop_no)

    return render(request, "shop/detail.html", {"shop": shop, "title": "Shop Detail"})
    


@login_required
def new_shop_form(request):
    if request.method == "GET":
        form = MyShopForm()
    else:
        form = MyShopForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Shop Creation Successful")
            return redirect('all-shops')
    return render(request, 'shop/new_shop_form.html', {'form':form})


@login_required
def edit_shop_form(request, shop_no):
    # Fetch the Shop instance using the shop number
    shop = get_object_or_404(Shop, no=shop_no)

    if request.method == 'POST':
        form = EditMyShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, "Shop details updated successfully")
            return redirect('all-shops')  # Redirect to the shop list or detail view
    else:
        form = EditMyShopForm(instance=shop)

    return render(request, 'shop/edit_shop_form.html', {'form': form})

def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def admin_edit_shop_form(request, shop_no):
    # Fetch the Shop instance using the shop number
    shop = get_object_or_404(Shop, no=shop_no)

    if request.method == 'POST':
        form = AdminEditMyShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, "Shop details updated successfully")
            return redirect('all-shops')  # Redirect to the shop list or detail view
    else:
        form = AdminEditMyShopForm(instance=shop)

    return render(request, 'shop/admin_edit_shop_form.html', {'form': form})


@login_required
def create_rent(request):
    if request.method == "POST":
        form = CreateRentForm(request.POST)
        due_date_str = request.POST.get("date_due")
        print("abdbd", due_date_str)
        # print(type(due_date))
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()


        if form.is_valid():
            form.save(commit=False)
            form.instance.date_due = due_date
            form.instance.is_paid = True
            form.instance.assigned_by = request.user
            form.instance.shop.status = "allocated"
            form.save()
            messages.success(request, "Rent creation successful")
            return redirect(reverse("list-shop-rents"))
        messages.error(request, "Something went wrong")
        return redirect(reverse("create-shop-rent"))
    else:
        form = CreateRentForm()
    context = {"form": form}
    return render(request, "rent/create_rent.html", context)


def list_rents(request):
    rents = Rent.objects.all()
    context = {"rents": rents}
    return render(request, "rent/list_rents.html", context)


def edit_rents(request, shop_no):
    rent = get_object_or_404(Rent, shop__no=shop_no)
    if request.method == "POST":
        form = EditMyRentForm(request.POST, instance=rent)
        if form.is_valid():
            form.save()
            messages.success(request, "Rent details updated successfully")
            return redirect(reverse("list-shop-rents"))
        else:
            messages.error(request, "Something went wrong")
            return redirect(reverse("edit-shop-rent", args=[shop]))
    else:
        form = EditMyRentForm(instance=rent)
    return render(request, "rent/edit_rent_form.html", {'form': form})


def send_rent_reminder(request, shop_no):
    rent = get_object_or_404(Rent, shop__no=shop_no)
    subject = 'Rent Reminder'
    message = f'Dear {rent.customer.name}, \n\n'\
              f'We hope this email finds you well. \n' \
              f'This is a friendly reminder that your rent for the month of is due on {rent.date_due}. Your payment is greatly appreciated and helps maintain the upkeep of our property.\n'\
              f'To avoid any late fees, please ensure your payment is received by the due date. You can make your payment through FCMB 9201562019 NINA SKY INNOVATIONS LTD.\n'\
              f"If you have any questions or require assistance, please don't hesitate to contact our office at (Phone Number)or (Email Address). \n"\
              f"Thank you for being a valued tenant.\n"\
              f"Sincerely,\n"\
              f"Nina Sky Innovation Limited"
    sender = settings.EMAIL_HOST_USER
    recipient = [rent.customer.email]
    send_mail(subject, message, sender, recipient, fail_silently=False)
    return HttpResponse("Email Successfully sent!")



@login_required
def upload_receipts(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid:
            form.save()
            existing_income = Income.objects.filter(name=form.cleaned_data["name"]).last()
            if form.cleaned_data["new_daily"] is not None:
                print("exisig", existing_income.daily)
                existing_income.daily += form.cleaned_data["new_daily"]
                existing_income.save()
            elif form.cleaned_data["new_weekly"] is not None:
                existing_income.weekly += form.cleaned_data["new_weekly"]
                existing_income.save()
            elif form.cleaned_data["new_weekly"] is not None:
                existing_income.yearly += form.cleaned_data["new_yearly"]
                existing_income.save()

            # if existing_income.new_daily is not None:
            #     existing_income.daily += form.cleaned_data["new_daily"]
            #     existing_income.save()
            #     existing_income.new_daily = Decimal('0.00')
            # elif existing_income.new_weekly is not None:
            #     existing_income.weekly +=  form.cleaned_data["new_weekly"]
            #     existing_income.save()
            #     existing_income.new_weekly = Decimal('0.00')
            # elif existing_income.new_yearly is not None:
            #     existing_income.yearly += form.cleaned_data["new_yearly"]
            #     existing_income.save()
            #     existing_income.new_yearly = Decimal("0.00")
            messages.success(request, "Amount successfully logged")
            return redirect(reverse("dashboard"))
        else:
            messages.error(request, "Couldn't complete upload")
            return redirect(reverse("income-upload"))
    else:
        form = IncomeForm()
    context = {
        "form": form
    }
    return render(request, "customer/upload_income.html", context)


@login_required
def view_payment_receipts(request):
    all_payments = PaymentSlip.objects.all()
    context = {"all_payments": all_payments}
    return render(request, "customer/all_income_uploads.html", context)

@login_required
def list_all_payment_receipts(request):
    all_receipts = PaymentSlip.objects.filter(is_verified=False)
    context = {
        "all_receipts": all_receipts
    }
    return render(request, "customer/list_all_receipts.html", context)

@login_required
def create_payment_slip(request):
    if request.method == 'POST':
        form = PaymentSlipForm(request.POST, request.FILES)
        if form.is_valid():
            payment_slip = form.save(commit=False)
            payment_slip.uploaded_by = request.user
            payment_slip.save()
            messages.success(request, "Receipt Upload Successful!")
            return redirect(reverse('list-all-uploaded-receipts'))
        else:
            return HttpResponse(form.errors)
    else:
        form = PaymentSlipForm()
    
    return render(request, 'customer/upload_customer_receipts.html', {'form': form})

@login_required
def receipt_list(request):
    """View to display all uploaded payment receipts."""
    # Get all payment receipts
    payment_account_filter = request.GET.get('payment_account', None)

    # Get all payment receipts, optionally filtered by payment account
    if payment_account_filter:
        payment_slips = PaymentSlip.objects.filter(payment_account=payment_account_filter).order_by("-payment_date")
    else:
        payment_slips = PaymentSlip.objects.all().order_by("-payment_date")

    # Pass the payment slips to the template
    return render(request, 'receipts/receipts_list.html', {'payment_slips': payment_slips,
                                                           'payment_account_choices': dict(PaymentSlip.PAYMENT_ACCOUNT_CHOICES).items(),
                                                           'selected_payment_account': payment_account_filter,})

@login_required
def verify_payment_receipt(request, pk):
    payment_slip = get_object_or_404(PaymentSlip, id=pk)
    payment_slip.is_verified = True
    payment_slip.save()
    messages.success(request, "Payment verified successfully")
    return redirect("list-all-uploaded-receipts")


@login_required
def review_payment_receipt(request, pk):
    payment_slip = get_object_or_404(PaymentSlip, id=pk)
    payment_slip.is_reviewed = True
    payment_slip.save()
    messages.success(request, "Payment has been reviewed successfully")
    return redirect("list-all-uploaded-receipts")

@login_required
def edit_payment_slip(request, pk):
    payment_slip = get_object_or_404(PaymentSlip, pk=pk)
    
    if request.method == 'POST':
        form = PaymentSlipEditForm(request.POST, request.FILES, instance=payment_slip)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment Data Saved")
            return redirect('all-receipts')
        else:
            messages.error(request, "Error saving payment data")
            return redirect(reverse("edit-uploaded-customer-payment", kwargs={"pk":pk}))
    else:
        form = PaymentSlipEditForm(instance=payment_slip)

    return render(request, 'customer/edit_customer_receipts.html', {'form': form})



@login_required
def generate_payment_advice(request, shop_no):
    shop = get_object_or_404(Shop, no=shop_no)
    return render(request, "shop/generate_shop_payment_advice.html", {"shop": shop})

@login_required
def generate_payment_advice_pdf(request, shop_no):
    shop = get_object_or_404(Shop, no=shop_no)
    html = render_to_string('shop/shop_pdf.html',
    {'shop': shop})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=payment_advice_{shop_no}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response


@login_required
def generate_payment_advice_old(request, shop_no):
    shop = get_object_or_404(Shop, no=shop_no)
    return render(request, "shop/generate_shop_payment_advice_old_customer.html", {"shop": shop})









    
