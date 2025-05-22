from django.db import models
from .models import Rent, Shop
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from decouple import config

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

    subject = "Rent Reminder"
    html_message = render_to_string("rent/30_days_reminder.html", {"customer": customer, "due_date": "2000-00-000"})
    plain_message = strip_tags(html_message)
    from_email = config("EMAIL_HOST_USER")  # Replace with your email
    to = customer.email
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
   

   
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
    subject = "Reminder: Your Rent Is Due Today"
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

@receiver(post_delete, sender=Rent)
def update_shop_status_on_rent_delete(sender, instance, **kwargs):
    """
    Updates the shop status to 'vacant' when its Rent is deleted.
    """
    shop = instance.shop
    shop.status = 'vacant'
    shop.is_paid = False  # Also reset payment status if needed
    shop.save()


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
        subject = "New Shop Created"
        html_message = render_to_string("shop/new_shop_email.html", {"shop": instance})
        plain_message = strip_tags(html_message)
        from_email = config("EMAIL_HOST_USER")  # Replace with your email
        to_emails = [user.email for user in User.objects.filter(is_superuser=True)]
        to = [user.email for user in User.objects.all() if user.is_superuser==True]
        send_mail(subject, plain_message, from_email, to_emails, html_message=html_message)
        



@receiver(post_save, sender=Rent)
def send_rent_creation_email(sender, instance, created, **kwargs):
    # if created:
    #     subject = 'Rent Paid !!'
    #     message = f'Dear {instance.customer.name},\n\n' \
    #               f'Your rent for the shop {instance.shop.no} has been created.\n' \
    #               f'Rent Type: {instance.rent_type}\n' \
    #               f'Rent Start Date: {instance.rent_start}\n' \
    #               f'Due Date: {instance.date_due}\n\n' \
    #               f'Thank you for your business!\n' \
    #               f'Best regards,\n' \
    #               f'Nina Sky Innovation Limited'
    #     sender = settings.EMAIL_HOST_USER
    #     recipient_list = [instance.customer.email]
    #     send_mail(subject, message, sender, recipient_list, fail_silently=False)

    if created:
        subject = "Shop Allocation Confirmation"
        html_message = render_to_string("rent/rent_allocation_email.html", {"shop": instance.shop, "rent": instance, "customer": instance.customer})
        plain_message = strip_tags(html_message)
        from_email = config("EMAIL_HOST_USER")
        to = [instance.customer.email]
        send_mail(subject, plain_message, from_email, to, html_message=html_message)



