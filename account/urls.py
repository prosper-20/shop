# from django.urls import path
# from . import views

from django.urls import path
from .views import create_user

urlpatterns = [
    path('create/', create_user, name='create_user'),
]

# urlpatterns = [
#     path('', views.account, name="account"),
#     path('form/', views.account_form, name="account_form"),
# ]

  