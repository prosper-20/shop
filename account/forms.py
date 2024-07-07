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

