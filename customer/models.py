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
        ('Restaurant', 'Restaurant'),
        ('Food and Drinks', 'Food and Drinks'),
        ('Makeup Artist', 'Makeup Artist'),
        ('Building', 'Building'),
        ('Tailoring', 'Tailoring'),
        ('Studio', 'Studio'),
        ('Beauty Salon', 'Beauty Salon'),
        ('Bakery', 'Bakery'),
        ('Wine Seller', 'Wine Seller'),
        ('Logistics', 'Logistics'),
        ('Clothing', 'Clothing'),
        ('Fabrics', 'Fabrics'),
        ('Oriflame Dealer', 'Oriflame Dealer'),
        ('Fruit Seller', 'Fruit Seller'),
        ('Communication', 'Communication'),
        ('Business Centre', 'Business Centre'),
        ('Bank', 'Bank'),
        ('Tv Repair', 'Tv Repair'),
        ('Hair Business', 'Hair Business'),
        ('Consultancy', 'Consultancy'),
        ('Skin Beauty Store', 'Skin Beauty Store'),
        ('Dispatch Office', 'Dispatch Office'),
        ('Loan Business', 'Loan Business'),
        ('Children Wears', 'Children Wears'),
        ('Electrical/Electronics Store', 'Electrical/Electronics Store'),
        ('Home Wears Store', 'Home Wears Store'),
        ('Travel Agency', 'Travel Agency'),
        ('Photo Studio', 'Photo Studio'),
        ('Law Firm', 'Law Firm'),
        ('Graphic Design and Branding', 'Graphic Design and Branding'),
        ('Perfumery', 'Perfumery'),
        ('NGO', 'NGO'),
        ("Others", "Others")
        
    ]

    STATUS = [
        ('new', 'New'),
        ('renewal', 'Renewal'),   
        ('exited', 'Exited'),    
    ]

    REVIWED_CHOICES = [
        ('Is Reviewed', 'Is Reviewed'),
        ('Not Reviewed', 'Not Reviewed')
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
    ("Zamfara", "Zamfara"),
    ("Others", "Others")
]
    
    TITLE_CHOICES = [
        ("Mr", "Mr"),
        ("Mrs", "Mrs"),
        ("Miss", "Miss"),
    ]

     
    no = models.CharField(max_length=4, unique=True)
    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default="Mr")
    name = models.CharField(max_length=100)
    business = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True)
    dob = models.DateField(default=None)
    address = models.CharField(max_length=225)
    state = models.CharField(max_length=225, choices=STATES)
    occupation = models.CharField(max_length=50)
    nature = models.CharField(max_length=255, choices=NATURE, default="")
    status = models.CharField(max_length=10, choices=STATUS, default='')
    is_reviewed = models.CharField(max_length=100, choices=REVIWED_CHOICES, default="Not Reviewed")
    date = models.DateField()
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    data_entry_officer_note = models.TextField(max_length=1000, blank=True, null=True)
    review_officer_note = models.TextField(max_length=1000, blank=True, null=True)
    approval_officer_note = models.TextField(max_length=1000, blank=True, null=True)
    approval =models.BooleanField(default=False)
    exitdate = models.DateField(blank=True, null=True)
    nextdue = models.DateField(blank=True, null=True)


    def __str__(self):
            return f"{self.title} {self.name}"
    
    class Meta:
          ordering = ["no"]
