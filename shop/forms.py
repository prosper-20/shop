from django import forms
from .models import Rate, Shop, Rent, Income,PaymentSlip
from datetime import timedelta, date
from customer.models import Customer


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
        fields = ('shop', 'customer',  'rent_type', 'amount_paid', 'date_paid', 'rent_start')
        labels = {
            'date_paid': 'Payment Date',
            'amount_paid': 'Amount Paid',
            'rent_start': 'Rent Start Date',
            'date_due': 'Rent Due Date',
            }
    
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
            'date_due': forms.DateInput(attrs={"type": 'date'}),
            'rent_start': forms.DateInput(attrs={"type": 'date'})
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter shops to only show vacant ones
        self.fields['shop'].queryset = Shop.objects.filter(status='vacant')

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
    # PAYMENT_ACCOUNT_CHOICES = [
    #     ('Nina Sky', 'Nina Sky'),
    #     ('Chairman', 'Chairman'),
    # ]

    # payment_account = forms.ChoiceField(
    #     choices=PAYMENT_ACCOUNT_CHOICES,
    #     label='Payment Account'
    # )

    narration = forms.CharField(
        max_length=255,
        required=False,  # This makes the field optional
        label='Narration (Optional)'
    )

    class Meta:
        model = PaymentSlip
        fields = ["payment_account", "customer", "amount", "shop_no", "image", "payment_date", "narration"]
        labels = {
            "shop_no": "Shop Number",
            "amount": "Amount",
            "image": "Upload Receipt (Optional)"
        }

        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for customer field
        self.fields['customer'].queryset = Customer.objects.all()
        # Set the widget to include an empty option
        self.fields['customer'].widget = forms.Select(
            choices=[('', 'Select a customer')] + [(c.id, f"{c.no} - {c.name}") for c in self.fields['customer'].queryset]
        )
        # Set initial value to None
        self.fields['customer'].initial = None
        self.fields['payment_date'].initial = date.today
        self.fields['payment_account'].initial = "Nina Sky"


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

    