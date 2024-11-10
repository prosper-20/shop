from django.db import models
from .models import Rent, Shop
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Rent, Customer

@receiver(post_save, sender=Rent)
def send_due_date_email(sender, instance, **kwargs):
    """Signal handler to send an email when the due date is 90 days from today."""
    # Calculate the current date and due date difference
    today = timezone.now().date()
    due_date = instance.date_due

    print("due_date", due_date)
    print("today", today)

    # Check if the due date is 90 days from today
    if due_date - today == timedelta(days=90):
        customer = instance.customer
        if customer.email:  # Ensure the customer has an email address
            send_due_date_reminder_email_90_days(customer)
    elif due_date - today == timedelta(days=60):
        customer = instance.customer
        if customer.email:  # Ensure the customer has an email address
            send_due_date_reminder_email_60_days(customer)
    elif due_date - today == timedelta(days=30):
        customer = instance.customer
        if customer.email:  # Ensure the customer has an email address
            send_due_date_reminder_email_30_days(customer)
    elif due_date - today == timedelta(days=7):
        customer = instance.customer
        if customer.email:  # Ensure the customer has an email address
            send_due_date_reminder_email_7_days(customer)
    elif due_date == today:
        customer = instance.customer
        if customer.email:  # Ensure the customer has an email address
            send_due_date_reminder_email_on_the_due_day(customer)
    




def send_due_date_reminder_email_90_days(customer):
    """Helper function to send the email."""
    subject = "Reminder: Your Rent Due Date is Approaching"
    message = f"Dear {customer.name},\n\n" \
              f"This is a friendly reminder that your rent payment is due in 90 days. Please ensure you make the necessary arrangements.\n\n" \
              f"Thank you for your attention to this matter.\n\n" \
              f"Best regards,\nNina Sky Innovation Limited"
    sender = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        sender,  # Sender's email (change to actual sender)
        [customer.email],
        fail_silently=False,
    )


def send_due_date_reminder_email_60_days(customer):
    """Helper function to send the email."""
    subject = "Reminder: Your Rent Due Date is Approaching"
    message = f"Dear {customer.name},\n\n" \
              f"This is a friendly reminder that your rent payment is due in 60 days. Please ensure you make the necessary arrangements.\n\n" \
              f"Thank you for your attention to this matter.\n\n" \
              f"Best regards,\nNina Sky Innovation Limited"
    sender = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        sender,  # Sender's email (change to actual sender)
        [customer.email],
        fail_silently=False,
    )


def send_due_date_reminder_email_30_days(customer):
    """Helper function to send the email."""
    subject = "Reminder: Your Rent Due Date is Approaching"
    message = f"Dear {customer.name},\n\n" \
              f"This is a friendly reminder that your rent payment is due in 30 days. Please ensure you make the necessary arrangements.\n\n" \
              f"Thank you for your attention to this matter.\n\n" \
              f"Best regards,\nNina Sky Innovation Limited"
    sender = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        sender,  # Sender's email (change to actual sender)
        [customer.email],
        fail_silently=False,
    )

def send_due_date_reminder_email_7_days(customer):
    """Helper function to send the email."""
    subject = "Reminder: Your Rent Due Date is Approaching"
    message = f"Dear {customer.name},\n\n" \
              f"This is a friendly reminder that your rent payment is due in 7 days. Please ensure you make the necessary arrangements.\n\n" \
              f"Thank you for your attention to this matter.\n\n" \
              f"Best regards,\nNina Sky Innovation Limited"
    sender = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        sender,  # Sender's email (change to actual sender)
        [customer.email],
        fail_silently=False,
    )

def send_due_date_reminder_email_on_the_due_day(customer):
    """Helper function to send the email."""
    subject = "Reminder: Your Rent Due Date is Approaching"
    message = f"Dear {customer.name},\n\n" \
              f"This is a friendly reminder that your rent payment is due today. Please ensure you make the necessary arrangements.\n\n" \
              f"Thank you for your attention to this matter.\n\n" \
              f"Best regards,\nNina Sky Innovation Limited"
    sender = settings.EMAIL_HOST_USER
    send_mail(
        subject,
        message,
        sender,  # Sender's email (change to actual sender)
        [customer.email],
        fail_silently=False,
    )

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


# @receiver(pre_save, sender=Rent)
# def check_due_date(sender, instance, **kwargs):
#     today = timezone.now().date()
#     if instance.date_due and instance.date_due <= today:
#         instance.is_expired = True
#     else:
#         instance.is_expired = False


@receiver(post_save, sender=Shop)
def send_email_on_shop_creation(sender, instance, created, **kwargs):
    if created:
        subject = 'New Shop Created'
        message = f'Hello sir, a new shop named {instance.no} has been created, Kindly review and approve it!'
        sender = settings.EMAIL_HOST_USER
        recipient = [user.email for user in User.objects.all() if user.is_superuser==True and user.is_approved==True]
        send_mail(subject, message, sender, recipient, fail_silently=False)



@receiver(post_save, sender=Rent)
def send_rent_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Rent Paid !!'
        message = f'Dear {instance.customer.name},\n\n' \
                  f'Your rent for the shop {instance.shop.no} has been created.\n' \
                  f'Rent Type: {instance.rent_type}\n' \
                  f'Rent Start Date: {instance.rent_start}\n' \
                  f'Due Date: {instance.date_due}\n\n' \
                  f'Thank you for your business!\n' \
                  f'Best regards,\n' \
                  f'Nina Sky Innovation Limited'
        sender = settings.EMAIL_HOST_USER
        recipient_list = [instance.customer.email]
        send_mail(subject, message, sender, recipient_list, fail_silently=False)



