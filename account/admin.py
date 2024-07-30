from django.contrib import admin
from .models import Role, CustomUser
from shop.models import Shop, Rate
from customer.models import Customer


class  CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_approved']


admin.site.register(CustomUser, CustomUserAdmin)

class RoleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Role, RoleAdmin)

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'address']

# # Register your models here.
# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('shop', 'date','customer', 'customer_date', 'name', 'shop_rent', 'shop_charges', 'rent_invoice', 'status')

#     exclude = ('shop_rent', 'shop_charges', 'rent_invoice')

#     def rent(self, obj):
#         Rate = obj.shop
#         return Rate.rent
        
#     def name(self, obj):
#         Customer = obj.customer
#         return Customer.name
    
#     def status(self, obj):
#         Customer = obj.customer
#         return Customer.status
    
#     def customer_date(self, obj):
#         Customer = obj.customer
#         return Customer.date
    
#     def shop_rent(self, obj):
#         Rate = obj.shop
#         return Rate.shop_rent

#     def shop_charges(self, obj):
#         Rate = obj.shop
#         return Rate.shop_charges
    
#     def shop_newcharges(self, obj):
#         Rate = obj.shop
#         return Rate.shop_newcharges
    
#     def rent_invoice(self, obj):
#         Customer.status = obj.customer.status
#         Rate = obj.shop
#         if Customer.status == 'new':
#             return Rate.new_rent
#         else:
#             return Rate.renewal_rent
    
#     def save_model(self, request, obj, form, change):
#         obj.shop_rent = self.shop_rent(obj)
#         obj.shop_charges = self.shop_charges(obj)
#         obj.rent_invoice = self.rent_invoice(obj)
#         super().save_model(request, obj, form, change)
    

# class ReceiptAdmin(admin.ModelAdmin):
#     list_display = ('shop', 'date','customer', 'rent_invoice_amount', 'amount', 'account', 'outstanding')

#     exclude = ('outstanding', 'rent_invoice_amount')

    

# admin.site.register(Account, AccountAdmin)
# admin.site.register(Receipt, ReceiptAdmin)