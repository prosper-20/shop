from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Rate, Shop
from django.db.models import Count
from .forms import ShopForm, MyShopForm, EditMyShopForm
from django.core.paginator import Paginator
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse

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






    
