from django.urls import path
from . import views
from web.views import home

urlpatterns = [
    
    path('', home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('shops/', views.myshops, name="all-shops"),
    path('shop/form/', views.shop_form, name="shop_form"),
    path('shop/create/', views.new_shop_form, name="shop-create"),
    path('shop/<int:id>', views.shop_form, name="shop_update"),

 
]

