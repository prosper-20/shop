from django import forms
from .models import Rate, Shop, Rent

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


class CreateRentForm(forms.ModelForm):
    class Meta:
        model = Rent
        fields = ('shop', 'customer', 'rent_type', 'is_paid', 'date_paid', 'is_expired', 'rent_start', 'date_due')

        




# 32,000.00
# 29,000.00
# 28,000.00
# 25,000.00
# 22,000.00
# 19,000.00

    