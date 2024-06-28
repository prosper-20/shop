from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout

# Create your views here.



def login_view(request):
    if request.method == "POST":
       form = AuthenticationForm(data=request.POST)
       if form.is_valid():
          login(request, form.get_user())
          return redirect("home")
       
    else:
       form = AuthenticationForm() 
    return render(request, "authentication/login.html", {"form":form})
    
def logout_view(request):
    form = AuthenticationForm(data=request.POST)
    if request.method =="POST":
       logout(request)
       return render(request, "authentication/logout.html", {"form": form})
