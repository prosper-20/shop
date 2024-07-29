from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Rate, Shop
from django.db.models import Count
from .forms import ShopForm, MyShopForm
from django.core.paginator import Paginator
from django.contrib import messages


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
            return redirect('shop')
    return render(request, 'shop/new_shop_form.html', {'form':form})





    
