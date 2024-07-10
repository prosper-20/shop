from django.contrib import admin
from .models import Shop, Rate
# Register your models here.

class RentAdmin(admin.ModelAdmin):
    list_display = ["shop", "customer", "rent_type", "date_paid", "date_due"]
    list_filter = ["customer", "rent_type", "date_due"]
    list_editable = ["managed_by"]

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class RateAdmin(admin.ModelAdmin):
    list_display = ('no', 'floor', 'price', 'size', 'get_rent', 'shop_price', 'shop_charges', 'shop_newcharges', 'status', 'new_rent', 'renewal_rent')

    exclude = ['status']

    def get_rent(self, obj):
        return obj.rent
    get_rent.short_description = 'Rent'

admin.site.register(Shop, ShopAdmin)
admin.site.register(Rate, RateAdmin)