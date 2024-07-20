from django.db import models
from .models import Rent
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=Rent)
def update_shop_status(sender, instance, created, **kwargs):
    if instance.is_paid and not instance.shop.status == 'vacant':
        instance.shop.status = 'allocated'
        instance.shop.save()



@receiver(post_save, sender=Rent)
def update_shop_is_paid(sender, instance, created, **kwargs):
    if created and instance.is_paid:
        shop = instance.shop
        shop.is_paid = True
        shop.status = "allocated"
        shop.save()


@receiver(post_save, sender=Rent)
def update_shop_is_not_paid(sender, instance, **kwargs):
    if instance.is_paid==False:
        shop = instance.shop
        shop.is_paid = False
        shop.status = "allocated"
        shop.save()

@receiver(post_save, sender=Rent)
def update_shop_is_not_paid_again(sender, instance, **kwargs):
    if instance.is_paid==True:
        shop = instance.shop
        shop.is_paid = True
        shop.status = "allocated"
        shop.save()


@receiver(pre_save, sender=Rent)
def check_due_date(sender, instance, **kwargs):
    today = timezone.now().date()
    if instance.date_due and instance.date_due <= today:
        instance.is_expired = True
    else:
        instance.is_expired = False