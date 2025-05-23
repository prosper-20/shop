from django.contrib import admin
from .models import Contact, ShopType


class ContactAdmin(admin.ModelAdmin):
    list_display = ["full_name", "email"]


admin.site.register(Contact, ContactAdmin)
admin.site.register(ShopType)
