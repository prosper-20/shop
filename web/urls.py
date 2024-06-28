from django.urls import path
from .views import custom_login, home


urlpatterns = [
    path('login/', custom_login, name='login'),
    path("home/", home, name="home")
]