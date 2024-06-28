from django import forms
from .models import Rate, Shop

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
    
    