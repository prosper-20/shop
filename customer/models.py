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

    STATES = [
    ("Abia", "Abia"),
    ("Adamawa", "Adamawa"),
    ("Akwa Ibom", "Akwa Ibom"),
    ("Anambra", "Anambra"),
    ("Bauchi", "Bauchi"),
    ("Bayelsa", "Bayelsa"),
    ("Benue", "Benue"),
    ("Borno", "Borno"),
    ("Cross River", "Cross River"),
    ("Delta", "Delta"),
    ("Ebonyi", "Ebonyi"),
    ("Edo", "Edo"),
    ("Ekiti", "Ekiti"),
    ("Enugu", "Enugu"),
    ("Gombe", "Gombe"),
    ("Imo", "Imo"),
    ("Jigawa", "Jigawa"),
    ("Kaduna", "Kaduna"),
    ("Kano", "Kano"),
    ("Katsina", "Katsina"),
    ("Kebbi", "Kebbi"),
    ("Kogi", "Kogi"),
    ("Kwara", "Kwara"),
    ("Lagos", "Lagos"),
    ("Nasarawa", "Nasarawa"),
    ("Niger", "Niger"),
    ("Ogun", "Ogun"),
    ("Ondo", "Ondo"),
    ("Osun", "Osun"),
    ("Oyo", "Oyo"),
    ("Plateau", "Plateau"),
    ("Rivers", "Rivers"),
    ("Sokoto", "Sokoto"),
    ("Taraba", "Taraba"),
    ("Yobe", "Yobe"),
    ("Zamfara", "Zamfara")
]

     
    no = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=100)
    business = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    dob = models.DateField(default=None)
    address = models.CharField(max_length=225)
    state = models.CharField(max_length=225, choices=STATES)
    occupation = models.CharField(max_length=50)
    nature = models.CharField(max_length=25, choices=NATURE, default="")
    status = models.CharField(max_length=10, choices=STATUS, default='')
    date = models.DateField()
    approval =models.BooleanField(default=False)
    exitdate = models.DateField()
    nextdue = models.DateField()


    def __str__(self):
            return self.name
