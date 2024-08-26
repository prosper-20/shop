from django import forms
from .models import Rate, Shop, Rent, Income,PaymentSlip
from datetime import timedelta

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["name", "new_daily", "new_weekly", "new_yearly"]
        labels = {
            "name": "Select Account",
            "new_daily": 'Daily Income',
            "new_weekly": "Weekly Income",
            "new_yearly": "Yearly Income"
        }

        
class ShopForm(forms.ModelForm):

    class Meta:
        model = Rate
        fields = ('no', 'floor', 'price', 'size')
        labels = {
            'no': 'Shop No',
            'floor': 'Shop Floor',
            'price': 'Shop Price',
            'size' : 'Shop Size',
        }

    def __init__(self, *args, **kwargs):
        super(ShopForm, self).__init__(*args, **kwargs)
        self.fields['price'].empty_label = "Select"
        self.fields['floor'].choices = [('', 'Select')] + list(self.fields['floor'].choices)



class MyShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('no', 'type', 'floor', 'price', 'size')
        labels = {
            'no': 'Shop No',
            'type': 'Shop Type',
            'floor': 'Shop Floor',
            'price': 'Shop Price',
            'size' : 'Shop Size',
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initial price set here in case of an existing instance
        if self.instance and self.instance.type:
            self.fields['price'].initial = self.instance.TYPE_PRICES.get(self.instance.type, 0)



class EditMyShopForm(forms.ModelForm): 
    class Meta:
        model = Shop
        fields = ('no', 'type', 'floor', 'price', 'size')
        labels = {
            'no': 'Shop No',
            'type': 'Shop Type',
            'floor': 'Shop Floor',
            'price': 'Shop Price',
            'size' : 'Shop Size',
        }



class AdminEditMyShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('no', 'type', 'floor', 'price', 'size', 'is_approved')
        labels = {
            'no': 'Shop No',
            'type': 'Shop Type',
            'floor': 'Shop Floor',
            'price': 'Shop Price',
            'size' : 'Shop Size',
            'is_approved': 'is Approved'
        }



class CreateRentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ('shop', 'customer', 'rent_type', 'date_paid', 'is_paid',  'rent_start', 'date_due', 'is_expired')
        labels = {
            'date_paid': 'Payment Date',
            'is_paid': 'Is Paid',
            'is_expired': 'Is Expired',
            'rent_start': 'Rent Start Date',
            'date_due': 'Rent Due Date',
            }
    
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
            'date_due': forms.DateInput(attrs={"type": 'date'}),
            'rent_start': forms.DateInput(attrs={"type": 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        rent_start = cleaned_data.get('rent_start')
        rent_type = cleaned_data.get('rent_type')

        if rent_start and rent_type:
            if rent_type == 'Monthly':
                # Calculate the date_due for monthly rent
                date_due = rent_start + timedelta(days=30)
            elif rent_type == 'Yearly':
                # Calculate the date_due for yearly rent
                date_due = rent_start + timedelta(days=365)
            elif rent_type == 'Lease':
                # Example: Assume a lease is for 6 months
                date_due = rent_start + timedelta(days=180)
            else:
                date_due = None  # Default if unknown rent_type

            cleaned_data['date_due'] = date_due

        return cleaned_data


class EditMyRentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ('shop', 'customer', 'rent_type', 'date_paid', 'is_paid',  'rent_start', 'date_due', 'is_expired')
        labels = {
            'date_paid': 'Payment Date',
            'is_paid': 'Is Paid',
            'is_expired': 'Is Expired',
            'rent_start': 'Rent Start Date',
            'date_due': 'Rent Due Date',
            }
        


class PaymentSlipForm(forms.ModelForm):
    PAYMENT_ACCOUNT_CHOICES = [
        ('Nina Sky', 'Nina Sky'),
        ('Chairman', 'Chairman'),
    ]

    payment_account = forms.ChoiceField(
        choices=PAYMENT_ACCOUNT_CHOICES,
        label='Payment Account'
    )
    class Meta:
        model = PaymentSlip
        fields = ["payment_account", "customer", "amount", "shop_no", "image"]
        labels = {
            "shop_no": "Shop Number",
            "amount": "Amount",
            "image": "Upload Receipt (Optional)"
        }


class PaymentSlipEditForm(forms.ModelForm):
    class Meta:
        model = PaymentSlip
        fields = ["customer", "amount", "shop_no", "image", "is_verified"]
        labels = {
            "shop_no": "Shop Number",
            "amount": "Amount",
            "image": "Upload Receipt (Optional)",
            "is_verified": "Confirm Payment"
        }


    
        




# 32,000.00
# 29,000.00
# 28,000.00
# 25,000.00
# 22,000.00
# 19,000.00

    