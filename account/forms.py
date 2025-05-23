from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Your password must contain at least 8 characters.",
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_number")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }


from django.contrib.auth.forms import (
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm,
)
from django import forms


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control",
                "placeholder": "Enter your email address",
            }
        ),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )


# from django import forms
# from .models import Account, Receipt

# class AccountForm(forms.ModelForm):

#     class Meta:
#         model = Account
#         fields = ('date', 'description', 'shop', 'customer', 'rent_invoice')
#         labels = {
#             'date': 'Invoice Date',
#             'description': 'Description',
#             'shop': 'Shop No',
#             'customer' : 'Customer ID',
#             'rent_invoice' : 'Rent Receivable',

#         }
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(AccountForm, self).__init__(*args, **kwargs)
#         self.fields['shop'].choices = [('', 'Select')] + list(self.fields['shop'].choices)
#         self.fields['customer'].choices = [('', 'Select')] + list(self.fields['customer'].choices)

# class ReceiptForm(forms.ModelForm):

#     class Meta:
#         model = Receipt
#         fields = ('date', 'invoice', 'shop', 'customer', 'account', 'amount', 'outstanding')
#         labels = {
#             'date': 'Payment Date',
#             'invoice': 'Invoice',
#             'shop': 'Shop No',
#             'customer' : 'Customer ID',
#             'account': 'Account Paid To',
#             'amount': 'Amount Received',


#         }
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),
#         }


# forms.py
