from django.contrib import admin
from .models import Customer


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("no", "name", "date", "status", "approval")
    list_filter = ["name", "status", "approval"]
    list_editable = ["approval", "status"]


admin.site.register(Customer, CustomerAdmin)
