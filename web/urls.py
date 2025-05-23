from django.urls import path
from .views import (
    staff_login,
    reviewer_entry_signup,
    data_entry_signup,
    staff_logout,
    home,
    dashboard,
    customer_login,
    create_customer,
    data_entry_dashbaord,
    review_officer_dashboard,
)
from customer.views import upload_customers


urlpatterns = [
    path("login/", customer_login, name="login"),
    path("signup/officer/", data_entry_signup, name="customer-signup"),
    path("signup/reviewer/", reviewer_entry_signup, name="reviewer-signup"),
    path("login/staff/", staff_login, name="staff-login"),
    path("logout/staff/", staff_logout, name="staff-logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("data-entry/dashboard/", data_entry_dashbaord, name="data-entry-dashboard"),
    path(
        "review-officer/dashboard/",
        review_officer_dashboard,
        name="review-officer-dashboard",
    ),
    path("home/", home, name="home"),
    path("upload/", upload_customers, name="upload"),
]


# path('edit-profile/', edit_profile, name='edit_profile'),
# path("userprofile/<str:username>/", new_profile, name="user-profile"),
# path('fetch-profile/', fetch_profile, name='fetch_profile'),
# path("profile/", view_profile, name="profile"),
# path("create/customer/", create_customer, name="create-customer"),
