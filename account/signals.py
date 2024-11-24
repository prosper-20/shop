from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model
import mailtrap as mt
from decouple import config
from customer.models import Customer
import mailtrap as mt
from decouple import config


User = get_user_model()

# @receiver(post_save, sender=Customer)
# def send_approval_email(sender, instance, **kwargs):
#     if instance.approval:
#         message = f""" 
#                         Hi {instance.name}, your account has been approved. """
#         mail = mt.Mail(
#             sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
#             to=[mt.Address(email=instance.email)],
#             subject="Account Approval",
#             text=message,
#             category="Integration Test",
#             )

#         client = mt.MailtrapClient(token=config("MAILTRAP_TOKEN"))
#         client.send(mail)

# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)



# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# @receiver(post_save, sender=User)
# def send_approval_email(sender, instance, **kwargs):
#     if instance.is_approved:
#         message = f""" 
#                             Hi {instance.username}, your account has been approved"""
#         mail = mt.Mail(
#                 sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
#                 to=[mt.Address(email=instance.email)],
#                 subject="Profile Approval",
#                 text=message,
#                 category="Integration Test",
#                 )

#         client = mt.MailtrapClient(token=config("MAILTRAP_TOKEN"))
#         client.send(mail)


# @receiver(post_save, sender=User)
# def send_creation_email(sender, created, instance, **kwargs):
#     if created:
#         message = f""" 
#                         Hi {instance.username}, your account has been created. Kindly wait for an
#                         approval email"""
#         mail = mt.Mail(
#             sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
#             to=[mt.Address(email=instance.email)],
#             subject="Signup Successful",
#             text=message,
#             category="Integration Test",
#             )

#         client = mt.MailtrapClient(token=config("MAILTRAP_TOKEN"))
#         client.send(mail)
    
    # mail = mt.Mail(
    #     sender=mt.Address(email="mailtrap@example.com", name="Mailtrap Test"),
    #     to=[mt.Address(email="your@email.com")],
    #     subject="You are awesome!",
    #     text="Congrats for sending test email with Mailtrap!",
    # )

    # # create client and send
    # client = mt.MailtrapClient(token="your-api-key")
    # client.send(mail)


# YOU COMMENTE THIS TWO ON SUNDAY


# @receiver(post_save, sender=Customer)
# def send_approval_email(sender, instance, created, **kwargs):
#     if instance.approval:
#         subject = 'Account Approved'
#         html_message = render_to_string('web/profile_approved_email.html', {'user': instance.name})
#         plain_message = strip_tags(html_message)
#         from_email = settings.EMAIL_HOST_USER
#         to_email = instance.email
#         send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)



# @receiver(post_save, sender=Customer)
# def send_creation_email(sender, instance, created, **kwargs):
#     if created:
#         subject = 'New Account'
#         message = f"Hello, a new customer named '{instance.name}' has been added. Kindly review and approve this account."
#         sender = settings.EMAIL_HOST_USER
#         recipient = [user.email for user in User.objects.all() if user.is_superuser==True and user.is_approved==True]
#         send_mail(subject, message, sender, recipient, fail_silently=False)