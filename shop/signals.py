from django.db import models
from .models import Rent
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=Rent)
def update_shop_status(sender, instance, created, **kwargs):
    if instance.is_paid and not instance.shop.status == 'vacant':
        instance.shop.status = 'allocated'
        instance.shop.save()
