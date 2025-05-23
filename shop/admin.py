from django.contrib import admin
from .models import Shop, Rate, Rent, Income, PaymentSlip


@admin.register(PaymentSlip)
class PaymentSlipAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "shop_no",
        "payment_date",
    )
    list_filter = ("shop_no", "payment_date")
    search_fields = ("shop_no", "payment_date")


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ["name", "daily", "weekly", "yearly"]
    list_filter = ["name"]
    search_fields = ["name"]


# Register your models here.


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ["shop", "customer", "rent_type", "date_paid", "date_due"]
    list_filter = ["customer", "rent_type", "date_due"]

    # def managed_by_username(self, obj):
    #     return str(obj.managed_by.username).upper()


class ShopAdmin(admin.ModelAdmin):
    list_display = ("no", "price", "floor", "type")
    list_filter = ("type", "price")
    list_editable = ("type", "floor")


class RateAdmin(admin.ModelAdmin):
    list_display = (
        "no",
        "floor",
        "price",
        "size",
        "get_rent",
        "shop_price",
        "shop_charges",
        "shop_newcharges",
        "status",
        "new_rent",
        "renewal_rent",
    )

    exclude = ["status"]

    def get_rent(self, obj):
        return obj.rent

    get_rent.short_description = "Rent"


admin.site.register(Shop, ShopAdmin)
admin.site.register(Rate, RateAdmin)
