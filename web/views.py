from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,  get_user_model
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.decorators import admin_required
# from .forms import RetrieveCustomerProfileForm
from shop.models import Shop, Rent
from customer.forms import CustomerForm
from customer.models import Customer

User = get_user_model()

def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_address')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            # if user.is_staff == False:
            #     messages.error(request, 'You are not authorized to login')
            #     return redirect(reverse('login'))
            # else:
                login(request, user)
                # Redirect to a success page, or wherever you want
                return redirect(reverse('dashboard'))  # Replace 'home' with your desired URL name
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(reverse('home'))
    else:
        return render(request, 'web/login.html')
    

def staff_logout(request):
    logout(request)
    return redirect("/web/home/") 
    


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_address')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page, or wherever you want
            return redirect(reverse('home'))  # Replace 'home' with your desired URL name
        else:
            messages.error(request, "Invalid email address or password.")
            return redirect(reverse('login'))
    else:
        return render(request, 'web/login.html')
    return render(request, 'web/login.html')


def customer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email_address')
        password = request.POST.get('password')
        password2 = request.POST.get("password2")

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered.')
                return redirect('signup')
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Account creation successful!")
                return redirect(reverse('login'))
        else:
            messages.error(request, "Both passwords must match!")
            return redirect(reverse('signup'))

    return render(request, 'web/customer_signup.html')


@login_required
def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(full_name=name, email=email, message=message)
        messages.success(request, "Thanks for reaching out")
        return redirect(reverse("home"))
    else:
        return render(request, "web/home.html")
    

@admin_required
def dashboard(request):
    users = User.objects.filter(is_staff=False)
    users_count = User.objects.filter(is_staff=False).count()
    no_of_due_rents = Rent.rents_due_count()
    no_of_paid_rents = Rent.rents_paid_count()
    no_of_shops = Shop.objects.all().count()
    all_customers = Customer.objects.all()
    all_customers_count = Customer.objects.all().count()
    allocated_shops = Shop.allocated_shops_count
    expected_rent_fees = Shop.expected_rent_fees
    sum_of_paid_rents = Shop.total_paid_shops_price()
    owing_customers = Rent.objects.filter(is_paid=False, shop__status="allocated")
    owing_customers_count = owing_customers.count()
    customers_awaiting_approval_count = Customer.objects.filter(approval=False).count()
    customers_awaiting_approval = Customer.objects.filter(approval=False)
    no_of_owing_shop_customers = Shop.objects.filter(status="allocated", is_paid=False).count()
    context = {"users": users, "users_count": users_count, "no_of_owing_shop_customers": no_of_owing_shop_customers, "customers_awaiting_approval": customers_awaiting_approval, "customers_awaiting_approval_count": customers_awaiting_approval_count, "all_customers": all_customers, "no_of_due_rents": no_of_due_rents, "no_of_paid_rents": no_of_paid_rents, "no_of_shops": no_of_shops, "allocated_shops": allocated_shops, "expected_rent_fees": expected_rent_fees, "sum_of_paid_rents": sum_of_paid_rents, "owing_customers": owing_customers, "owing_customers_count": owing_customers_count, "all_customers_count": all_customers_count, "current_user": request.user}
    return render(request, "web/dashboard.html", context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from account.models import Profile
# from .forms import ProfileEditForm


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


# @login_required
# def view_profile(request):
#     # Retrieve the profile associated with the current logged-in user
#     profile = get_object_or_404(Profile, user=request.user)

#     if request.method == 'POST':
#         form = ProfileEditForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect(reverse('profile'))  # Redirect to profile view page after saving
#     else:
#         form = ProfileEditForm(instance=profile)

#     return render(request, 'web/new_profile.html', {'form': form, 'profile': profile})
    
    # Render the profile details in a template
    # return render(request, 'web/profile.html', {'profile': profile})
    # return render(request, 'web/new_profile.html', {'profile': profile})


# @login_required
# def edit_profile(request):
#     profile = get_object_or_404(Profile, user=request.user)

    

#     if request.method == 'POST':
#         form = ProfileEditForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect(reverse('profile'))  # Redirect to profile view page after saving
#     else:
#         form = ProfileEditForm(instance=profile)

#     return render(request, 'web/new_profile.html', {'form': form})



# @login_required
# def new_profile(request, *args, **kwargs):
#     username = kwargs.get("username")
#     print(username)
#     profile = get_object_or_404(Profile, user__username=username)

#     if request.method == 'POST':
#         form = ProfileEditForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect(reverse('profile'))  # Redirect to profile view page after saving
#     else:
#         form = ProfileEditForm(instance=profile)

#     return render(request, 'web/new_profile.html', {'form': form, 'profile': profile})



# if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST,
#                                    request.FILES,
#                                    instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('profile')

#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }

#     return render(request, 'users/profile.html', context)


# @admin_required
# def fetch_profile(request):
#     if request.method == 'POST':
#         form = RetrieveCustomerProfileForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             try:
#                 user = get_object_or_404(User, email=email)
#                 profile = get_object_or_404(Profile, user=user)
#                 form = ProfileEditForm(instance=profile)
#                 return render(request, 'web/new_profile.html', {'profile': profile, "form": form})
#             except User.DoesNotExist:
#                 error_message = "User with this email does not exist."
#                 return render(request, 'web/new_profile.html', {'form': form, 'error_message': error_message})
#             except Profile.DoesNotExist:
#                 error_message = "Profile does not exist for this user."
#                 return render(request, 'web/new_profile.html', {'form': form, 'error_message': error_message})
#     else:
#         form = RetrieveCustomerProfileForm()
    
#     return render(request, 'web/fetch_profile.html', {'form': form})


@admin_required
def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, "Customer created successfully!")
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, "Something went wrong!")
            return render(request, 'web/my_customer_signup_form.html', {'form': form})
    else:
        form = CustomerForm()
    return render(request, "web/my_customer_signup_form.html", {"form": form})










