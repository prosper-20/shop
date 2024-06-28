from django.db import models
from datetime import date

# Create your models here.
class Customer(models.Model):

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
     
    no = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    business = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=18)
    dob = models.DateField(default=None)
    address = models.CharField(max_length=225)
    state = models.CharField(max_length=225, default='')
    occupation = models.CharField(max_length=50)
    nature = models.CharField(max_length=25, choices=NATURE, default="")
    status = models.CharField(max_length=10, choices=STATUS, default='')
    date = models.DateField()
    approval =models.BooleanField(default=False)
    exitdate = models.DateField(null=True, blank=True, default=None)
    nextdue = models.DateField(null=True, blank=True, default=None)


    def __str__(self):
            return self.no
