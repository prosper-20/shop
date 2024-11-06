from django.urls import path
from . import views
from web.views import home, dashboard

urlpatterns = [
    path('', dashboard, name="home-dashboard"),
    path('shop/', views.shop, name="shop"),
    path('shop/generate/', views.generate_shops, name="generate"),
    path('shops/', views.myshops, name="all-shops"),
    path('shop/create/', views.new_shop_form, name="shop-create"),
    path("shop/rent/create/", views.create_rent, name="create-shop-rent"),
    path("shop/rent/edit/<str:shop_no>/", views.edit_rents, name="edit-shop-rents"),
    path("shop/rent/<str:shop_no>/reminder/", views.send_rent_reminder, name="send-rent-reminder"),
    path("shop/rents/", views.list_rents, name="list-shop-rents"),
    path('shops/<str:shop_no>/', views.edit_shop_form, name="shop-edit"),
    path('shop/form/', views.shop_form, name="shop_form"),
    path('shop/<int:id>', views.shop_form, name="shop_update"),
    path('shop/edit/<str:shop_no>/', views.admin_edit_shop_form, name="admin-edit-shop-form"),
    path('shop/<str:shop_no>/generate-invoice/', views.generate_payment_advice, name="generate-shop-paymrnt-advice"),
    path('shop/<str:shop_no>/generate-invoice/old/', views.generate_payment_advice_old, name="generate-payment-advice-old"),
    path('shop/<str:shop_no>/generate-invoice/pdf/', views.generate_payment_advice_pdf, name="generate-shop-payment-advice-pdf"),
    path("income/upload/", views.upload_receipts, name="income-upload"),
    path("upload/receipts/", views.create_payment_slip, name="upload-customer-payment"),
    path("receipts/<int:pk>/", views.edit_payment_slip, name="edit-uploaded-customer-payment"),
    path("receipts/all/", views.list_all_payment_receipts, name="all-receipts"),
    path("paymentslips/all/", views.view_payment_receipts, name="all-payment-slips"),
    path("all/uploaded-receipts/", views.receipt_list, name="list-all-uploaded-receipts")

 
]

