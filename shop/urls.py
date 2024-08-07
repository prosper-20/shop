from django.urls import path
from . import views
from web.views import home

urlpatterns = [
    path('', home, name="home"),
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
    path("income/upload/", views.upload_receipts, name="income-upload")

 
]

