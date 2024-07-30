from django.db import models
from customer.models import Customer
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=25)
    email = models.EmailField(_("email address"), unique=True)
    is_approved = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

# class Account(models.Model):

#     STATUS = [
#         ('Unpaid', 'Unpaid'),
#         ('Paid', 'Paid'),
#     ]

#     date = models.DateField()
#     description = models.CharField(max_length=150)
#     shop = models.ForeignKey(Rate, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     shop_rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     shop_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     rent_invoice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     status = models.CharField(max_length=10, choices=STATUS, default="Unpaid")

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             # Set the customer status to 'pending'
#             self.customer.status = 'pending'
#             self.customer.date += timedelta(days=365)  # Add 365 days to the customer date
#             self.customer.save()

#         if not self.pk:
#             # Set the customer status to 'renewal'
#             self.customer.status = 'renewal'
#             self.customer.save()
#         # Call the original save method
#         super(Account, self).save(*args, **kwargs)

#         # Update the status of the related Rate object to 'Allocated'
#         if self.shop.status != 'active':  # Check if status is not already 'active'
#             self.shop.status = 'active'
#             self.shop.save()
    
#     def calculate_outstanding_balance(self):
#         total_received = self.receipt_set.aggregate(total=models.Sum('amount'))['total'] or 0
#         return self.rent_invoice - total_received

#     def __str__(self):
#         return f'{self.customer.no}-{self.shop.no}-{self.description}'
    
# class Receipt(models.Model):

#     ACCOUNT = [
#         ('Nina Sky', 'Nina'),
#         ('Chairman', 'Chairman'),   
#     ]

#     date = models.DateField()
#     invoice = models.OneToOneField(Account, on_delete=models.CASCADE)
#     shop = models.CharField(max_length=4)
#     customer = models.CharField(max_length=5)
#     amount = models.DecimalField(max_digits=20, decimal_places=2)
#     account = models.CharField(max_length=20, choices=ACCOUNT, default="Nina Sky")
#     rent_invoice_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     outstanding = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def save(self, *args, **kwargs):
#         # Update rent_invoice_amount and outstanding
#         self.rent_invoice_amount = self.invoice.rent_invoice
#         total_received = self.invoice.receipt_set.aggregate(total=models.Sum('amount'))['total'] or 0
#         self.outstanding = self.rent_invoice_amount - self.amount
        
#         super(Receipt, self).save(*args, **kwargs)

#         # Update Account status to 'Paid' if fully paid
#         if self.invoice.calculate_outstanding_balance() <= 0:
#             self.invoice.status = 'Paid'
#             self.invoice.save()


class Role(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.name


NATURE = [
        ('Supermarket', 'Supermarket'),
        ('Laundry', 'Laundry'),
        ('Pharmacy', 'Pharmacy'),
        ('Courier/Dispatch', 'Courier/Dispatch'),
        ('Banking/Insurance', 'Banking/Insurance'),
        ('Barbing/Salon', 'Barbing/Salon'),
        
    ]

STATUS = [
        ('new', 'new'),
        ('renewal', 'renewal'),   
        ('exited', 'exited'),    
    ]

# class Profile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     address = models.CharField(max_length=100, blank=True, null=True)
#     image = models.ImageField(default="user.jpg", upload_to="profile_pics")
#     dob = models.DateField(default=None)
#     address = models.CharField(max_length=225)
#     state = models.CharField(max_length=225, default='')
#     occupation = models.CharField(max_length=50)
#     nature = models.CharField(max_length=25, choices=NATURE, default="")
#     status = models.CharField(max_length=10, choices=STATUS, default='')

#     def __str__(self):
#         return self.user.username

    
