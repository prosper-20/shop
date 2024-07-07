from django.urls import path
from .views import staff_login, customer_signup, home, dashboard, customer_login


urlpatterns = [
    path("login/customer/", customer_login, name="login"),
    path("signup/customer/", customer_signup, name='customer-signup'),
    path('login/staff/', staff_login, name='staff-login'),
    path("dashboard/", dashboard, name="dashboard"),
    path("home/", home, name="home")
]