from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from .models import Contact
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

User = get_user_model()

def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('email_address')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page, or wherever you want
            return redirect(reverse('dashboard'))  # Replace 'home' with your desired URL name
        else:
            messages.error(request, "Invalid username or password.")
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
            return redirect(reverse('dashboard'))  # Replace 'home' with your desired URL name
        else:
            messages.error(request, "Invalid username or password.")
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
    


def dashboard(request):
    users = User.objects.all()
    users_count = users.count()
    return render(request, "web/dashboard.html", {"users": users, "users_count": users_count})






