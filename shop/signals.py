from django.db import models
from .models import Rent, Shop
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

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


@receiver(post_save, sender=Shop)
def send_email_on_shop_creation(sender, instance, created, **kwargs):
    if created:
        subject = 'New Shop Created'
        message = f'Hello sir, a new shop named {instance.no} has been created, Kindly review and approve it!'
        sender = settings.EMAIL_HOST_USER
        recipient = [user.email for user in User.objects.all() if user.is_superuser==True and user.is_approved==True]
        send_mail(subject, message, sender, recipient, fail_silently=False)



