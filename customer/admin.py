from django.contrib import admin
from .models import Customer

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'date', 'status', 'approval')


admin.site.register(Customer, CustomerAdmin)