from django.db import models
from .models import Rent
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from customer.models import Customer
from django.utils import timezone
from django.contrib.auth import get_user_model
