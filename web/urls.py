from django.urls import path
from .views import staff_login, customer_signup, staff_logout, home, dashboard, customer_login, create_customer

urlpatterns = [
    path("login/customer/", customer_login, name="login"),
    path("signup/customer/", customer_signup, name='customer-signup'),
    # path("create/customer/", create_customer, name="create-customer"),
    path('login/staff/', staff_login, name='staff-login'),
    path('logout/staff/', staff_logout, name='staff-logout'),
    path("dashboard/", dashboard, name="dashboard"),
    # path('edit-profile/', edit_profile, name='edit_profile'),
    # path("userprofile/<str:username>/", new_profile, name="user-profile"),
    # path('fetch-profile/', fetch_profile, name='fetch_profile'),
    # path("profile/", view_profile, name="profile"),
    path("home/", home, name="home")

]


