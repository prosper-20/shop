from django.urls import path
from .views import custom_login, home, dashboard


urlpatterns = [
    path('login/', custom_login, name='login'),
    path("dashboard/", dashboard, name="dashboard"),
    path("home/", home, name="home")
]