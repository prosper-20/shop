from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages


def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False  # Default approval status
            user.save()
            messages.success(request, 'User created successfully! Pending approval.')
            return redirect('user_list')  # Redirect to user list view
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'account/create_user.html', {'form': form})




# from .forms import AccountForm, ReceiptForm
# from .models import Account,Receipt
# Create your views here.
# @login_required
# def account(request):
#     accountlist = Account.objects.all()
#     if request.method == 'POST':
#         form = AccountForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Invoice posted for customer shop rent successfully.')
#             return redirect('account')  # Redirect to the same page to show the success message
#     else:
#         form = AccountForm()

#     return render(request, 'account/account.html', {'form': form, 'accountlist' : accountlist} )

# @login_required
# def account_form(request):
#     accountlist = Receipt.objects.all()
#     if request.method == 'POST':
#         form = ReceiptForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Amount received successfully posted  as rent paid by customer.')
#             return redirect('account')  # Redirect to the same page to show the success message
#     else:
        
#         form = ReceiptForm()
#     return render(request, 'account/account_form.html', {'form': form})



# views.py


