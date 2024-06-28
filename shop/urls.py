from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.home, name="home"),
    path('shop/', views.shop, name="shop"),
    path('shop/form/', views.shop_form, name="shop_form"),
    path('shop/<int:id>', views.shop_form, name="shop_update"),

 
]

