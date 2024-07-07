from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from account.decorators import admin_required
from .forms import RetrieveCustomerProfileForm
from shop.models import Shop

User = get_user_model()

def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_address')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff == False:
                messages.error(request, 'You are not authorized to login')
                return redirect(reverse('login'))
            else:
                login(request, user)
                # Redirect to a success page, or wherever you want
                return redirect(reverse('dashboard'))  # Replace 'home' with your desired URL name
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(reverse('home'))
    else:
        return render(request, 'web/login.html')
    


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
            return redirect(reverse('login'))

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
    users = User.objects.all()
    users_count = users.count()
    no_of_owing_shop_customers = Shop.objects.filter(status="allocated", is_paid=False).count()
    context = {"users": users, "users_count": users_count, "no_of_owing_shop_customers": no_of_owing_shop_customers}
    return render(request, "web/dashboard.html", context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.models import Profile
from .forms import ProfileEditForm


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from account.models import Profile

@login_required
def view_profile(request):
    # Retrieve the profile associated with the current logged-in user
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(reverse('profile'))  # Redirect to profile view page after saving
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'web/new_profile.html', {'form': form, 'profile': profile})
    
    # Render the profile details in a template
    # return render(request, 'web/profile.html', {'profile': profile})
    return render(request, 'web/new_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(reverse('profile'))  # Redirect to profile view page after saving
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'web/new_profile.html', {'form': form})



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


@admin_required
def fetch_profile(request):
    if request.method == 'POST':
        form = RetrieveCustomerProfileForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = get_object_or_404(User, email=email)
                profile = get_object_or_404(Profile, user=user)
                form = ProfileEditForm(instance=profile)
                return render(request, 'web/new_profile.html', {'profile': profile, "form": form})
            except User.DoesNotExist:
                error_message = "User with this email does not exist."
                return render(request, 'web/new_profile.html', {'form': form, 'error_message': error_message})
            except Profile.DoesNotExist:
                error_message = "Profile does not exist for this user."
                return render(request, 'web/new_profile.html', {'form': form, 'error_message': error_message})
    else:
        form = RetrieveCustomerProfileForm()
    
    return render(request, 'web/fetch_profile.html', {'form': form})










