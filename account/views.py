from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView
)
from .forms import (
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomPasswordChangeForm
)
from django.views import View
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from decouple import config
from django.urls import reverse

User = get_user_model()

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


class CustomPasswordResetView(View):
    def get(self, request):
        return render(request, "account/password_reset.html")
    
    def post(self, request):
        email = request.POST.get("email")
        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email not found")
            return redirect("password_reset")
        else:
            user = get_object_or_404(User, email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://127.0.0.1:8000/accounts/password-reset/confirm/{uid}/{token}/"
            subject = "Password Reset!"
            html_message = render_to_string(
            "account/password_reset_email.html",
            {"uid": uid, "token": token, "reset_link": reset_link},
        )
            plain_message = strip_tags(html_message)
            from_email = config("DEFAULT_FROM_EMAIL")  # Replace with your email
            to = email
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            messages.success(request, "A link has been sent to your email")
            return redirect("password_reset_done")
        


# class CustomPasswordResetView(PasswordResetView):
#     form_class = CustomPasswordResetForm
#     template_name = 'account/password_reset.html'
#     email_template_name = 'account/password_reset_email.html'
#     subject_template_name = 'account/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class CustomPasswordResetConfirmView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            return render(request, 'account/password_reset_page.html', {
                'uidb64': uidb64,
                'token': token,
                'validlink': True
            })
        else:
            messages.error(request, "Password reset link is invalid or has expired")
            return redirect('password_reset')
    
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            password = request.POST.get("password")
            password2 = request.POST.get("password2")
            
            if password != password2:
                messages.error(request, "Passwords do not match")
                return render(request, 'account/password_reset_page.html', {
                    'uidb64': uidb64,
                    'token': token,
                    'validlink': True
                })
            
            # Set the new password
            user.set_password(password)
            user.save()
            
            messages.success(request, "Password has been reset successfully")
            return redirect("password_reset_complete")
        else:
            messages.error(request, "Password reset link is invalid or has expired")
            return redirect('password_reset')

            
            

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'




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