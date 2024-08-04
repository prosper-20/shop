from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Rate, Shop, Rent
from django.db.models import Count
from .forms import ShopForm, MyShopForm, EditMyShopForm, EditMyRentForm, CreateRentForm
from django.core.paginator import Paginator
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail


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
    all_shops = Shop.objects.all()
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



def create_rent(request):
    if request.method == "POST":
        form = CreateRentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rent successfully logged!")
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







    
