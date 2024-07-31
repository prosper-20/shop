from django.urls import path
from . import views
from web.views import home

urlpatterns = [
    
    path('', home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('shop/generate/', views.generate_shops, name="generate"),
    path('shops/', views.myshops, name="all-shops"),
    path('shop/create/', views.new_shop_form, name="shop-create"),
    path('shops/<str:shop_no>/', views.edit_shop_form, name="shop-edit"),
    path('shop/form/', views.shop_form, name="shop_form"),
    path('shop/<int:id>', views.shop_form, name="shop_update"),

 
]

