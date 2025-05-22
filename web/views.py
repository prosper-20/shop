from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,  get_user_model
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from account.decorators import admin_required
from shop.models import Shop, Rent, Income
from customer.forms import CustomerForm
from customer.models import Customer

User = get_user_model()


def is_review_officer(user):
    return user.is_staff

def is_admin_officer(user):
    return user.is_superuser

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
            if user.is_staff and not user.is_superuser:
                return redirect(reverse('review-officer-dashboard'))
            elif user.is_superuser:
                return redirect(reverse('dashboard'))
            else:
                return redirect(reverse('data-entry-dashboard'))  # Replace 'home' with your desired URL name
        else:
            messages.error(request, "Invalid email address or password.")
            return redirect(reverse('login'))
    else:
        return render(request, 'web/login.html')


def data_entry_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email_address')
        phone_number = request.POST.get("phone_number")
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
                User.objects.create_user(username=username, email=email, phone_number=phone_number, password=password)
                messages.success(request, "Account creation successful!")
                return redirect(reverse('login'))
        else:
            messages.error(request, "Both passwords must match!")
            return redirect(reverse('signup'))

    return render(request, 'web/data_entry_officer_signup.html')


def reviewer_entry_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email_address')
        phone_number = request.POST.get("phone_number")
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
                User.objects.create_user(username=username, email=email, phone_number=phone_number, password=password, is_staff=True)
                messages.success(request, "Account creation successful!")
                return redirect(reverse('login'))
        else:
            messages.error(request, "Both passwords must match!")
            return redirect(reverse('signup'))

    return render(request, 'web/review_officer_signup.html')


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
    

@login_required
def data_entry_dashbaord(request):
    users = User.objects.filter(is_staff=False)
    users_count = User.objects.filter(is_staff=False).count()
    no_of_due_rents = Rent.rents_due_count()
    no_of_paid_rents = Rent.rents_paid_count()
    no_of_shops = Shop.objects.all().count()
    all_customers = Customer.objects.all()
    allocated_shops = Shop.allocated_shops_count
    expected_rent_fees = Shop.expected_rent_fees
    sum_of_paid_rents = Shop.total_paid_shops_price()
    owing_customers = Rent.objects.filter(is_paid=False, shop__status="allocated")
    customers_awaiting_review = Customer.objects.filter(is_reviewed=False)
    customers_awaiting_approval = Customer.objects.filter(approval=False)
    no_of_owing_shop_customers = Shop.objects.filter(status="allocated", is_paid=False).count()

    context = {"users": users, "daily_income_total": 0,
                "weekly_income_total": 0,
                "yearly_income_total": 0,
                "nina_daily_income": 0, "nina_weekly_income":0, 
                "nina_yearly_income": 0, 
                "chairman_daily_income": 0, 
                "chairman_weekly_income": 0, 
                "chairman_yearly_income": 0, 
                "users_count": users_count, "no_of_owing_shop_customers": no_of_owing_shop_customers,
                "customers_awaiting_approval": customers_awaiting_approval,
                "customers_awaiting_review": customers_awaiting_review,
                "all_customers": all_customers, "no_of_due_rents": no_of_due_rents, 
                "no_of_paid_rents": no_of_paid_rents, "no_of_shops": no_of_shops, 
                "allocated_shops": allocated_shops, "expected_rent_fees": expected_rent_fees,
                "sum_of_paid_rents": sum_of_paid_rents,
                "owing_customers": owing_customers, 
                    
                "current_user": request.user, "all_income": 0}
    
    return render(request, "web/data_entry_dashboard.html", context)


@user_passes_test(is_review_officer)
def review_officer_dashboard(request):
    users = User.objects.filter(is_staff=False)
    users_count = User.objects.filter(is_staff=False).count()
    no_of_due_rents = Rent.rents_due_count()
    no_of_paid_rents = Rent.rents_paid_count()
    no_of_shops = Shop.objects.all().count()
    all_customers = Customer.objects.all()
    allocated_shops = Shop.allocated_shops_count
    expected_rent_fees = Shop.expected_rent_fees
    sum_of_paid_rents = Shop.total_paid_shops_price()
    owing_customers = Rent.objects.filter(is_paid=False, shop__status="allocated")
    customers_awaiting_review = Customer.objects.filter(is_reviewed=False)
    customers_awaiting_approval = Customer.objects.filter(approval=False)
    no_of_owing_shop_customers = Shop.objects.filter(status="allocated", is_paid=False).count()

    context = {"users": users, "daily_income_total": 0,
                "weekly_income_total": 0,
                "yearly_income_total": 0,
                "nina_daily_income": 0, "nina_weekly_income":0, 
                "nina_yearly_income": 0, 
                "chairman_daily_income": 0, 
                "chairman_weekly_income": 0, 
                "chairman_yearly_income": 0, 
                "users_count": users_count, "no_of_owing_shop_customers": no_of_owing_shop_customers,
                "customers_awaiting_approval": customers_awaiting_approval,
                "customers_awaiting_review": customers_awaiting_review,
                "all_customers": all_customers, "no_of_due_rents": no_of_due_rents, 
                "no_of_paid_rents": no_of_paid_rents, "no_of_shops": no_of_shops, 
                "allocated_shops": allocated_shops, "expected_rent_fees": expected_rent_fees,
                "sum_of_paid_rents": sum_of_paid_rents,
                "owing_customers": owing_customers, 
                    
                "current_user": request.user, "all_income": 0}
    
    return render(request, "web/review_officer_dashboard.html", context)

@user_passes_test(is_admin_officer)
def dashboard(request):
    if request.method == "POST":
        searched = request.POST.get("search_term")
        results = Customer.objects.filter(name__icontains=searched)
    else:
        users = User.objects.filter(is_staff=False)
        users_count = User.objects.filter(is_staff=False).count()
        no_of_due_rents = Rent.rents_due_count()
        no_of_paid_rents = Rent.rents_paid_count()
        no_of_shops = Shop.objects.all().count()
        all_customers = Customer.objects.all()
        allocated_shops = Shop.allocated_shops_count
        expected_rent_fees = Shop.expected_rent_fees
        sum_of_paid_rents = Rent.total_paid_shops_price()
        owing_customers = Rent.objects.filter(is_expired=True, is_paid=True, shop__status="allocated")
        customers_awaiting_review = Customer.objects.filter(is_reviewed=False)
        customers_awaiting_approval = Customer.objects.filter(approval=False)
        no_of_owing_shop_customers = Shop.objects.filter(status="allocated", is_paid=False).count()
        # all_income = Income.objects.all()
        # nina_daily_income = get_object_or_404(Income, name="Nina").daily
        # nina_weekly_income = get_object_or_404(Income, name="Nina").weekly
        # nina_yearly_income = get_object_or_404(Income, name="Nina").yearly
        # chairman_daily_income = get_object_or_404(Income, name="Chairman").daily
        # chairman_weekly_income = get_object_or_404(Income, name="Chairman").weekly
        # chairman_yearly_income = get_object_or_404(Income, name="Chairman").yearly
        # daily_income_total = Income.total_daily_receipts()
        # weekly_income_total = Income.total_weekly_receipts()
        # yearly_income_total = Income.total_yearly_receipts()
        # context = {"users": users, "daily_income_total": daily_income_total,
        #         "weekly_income_total": weekly_income_total,
        #         "yearly_income_total": yearly_income_total,
        #             "nina_daily_income": nina_daily_income, "nina_weekly_income":nina_weekly_income, 
        #             "nina_yearly_income": nina_yearly_income, 
        #             "chairman_daily_income": chairman_daily_income, 
        #             "chairman_weekly_income": chairman_weekly_income, 
        #             "chairman_yearly_income": chairman_yearly_income, 
        #             "users_count": users_count, "no_of_owing_shop_customers": no_of_owing_shop_customers,
        #             "customers_awaiting_approval": customers_awaiting_approval,
        #             "customers_awaiting_approval_count": customers_awaiting_approval_count,
        #             "all_customers": all_customers, "no_of_due_rents": no_of_due_rents, 
        #             "no_of_paid_rents": no_of_paid_rents, "no_of_shops": no_of_shops, 
        #             "allocated_shops": allocated_shops, "expected_rent_fees": expected_rent_fees,
        #             "sum_of_paid_rents": sum_of_paid_rents,
        #             "owing_customers": owing_customers, "owing_customers_count": owing_customers_count,
        #             "all_customers_count": all_customers_count, 
        #             "current_user": request.user, "all_income": 0}


        context = {"users": users, "daily_income_total": 0,
                "weekly_income_total": 0,
                "yearly_income_total": 0,
                    "nina_daily_income": 0, "nina_weekly_income":0, 
                    "nina_yearly_income": 0, 
                    "chairman_daily_income": 0, 
                    "chairman_weekly_income": 0, 
                    "chairman_yearly_income": 0, 
                    "users_count": users_count, "no_of_owing_shop_customers": no_of_owing_shop_customers,
                    "customers_awaiting_approval": customers_awaiting_approval,
                    "customers_awaiting_review": customers_awaiting_review,
                    "all_customers": all_customers, "no_of_due_rents": no_of_due_rents, 
                    "no_of_paid_rents": no_of_paid_rents, "no_of_shops": no_of_shops, 
                    "allocated_shops": allocated_shops, "expected_rent_fees": expected_rent_fees,
                    "sum_of_paid_rents": sum_of_paid_rents,
                    "owing_customers": owing_customers, 
                     
                    "current_user": request.user, "all_income": 0}
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


@login_required
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










