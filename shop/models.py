from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth import get_user_model
User = get_user_model()

class Shop(models.Model):
 
    Type = [
        ('A', 'Type A'),
        ('B', 'Type B'),
        ('C', 'Type C'),
        ('D', 'Type D'),
        ('E', 'Type E'),
        ('F', 'Type F'),
    ]

    Floor = [
        ('G', 'Ground Floor'),
        ('1', 'First Floor'),
        ('2', 'Second Floor'),
       
    ]

    STATUS = [
        ('vacant', 'Vacant'),
        ('allocated', 'Allocated'),
     
       
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    no = models.CharField(max_length=5, default=0)
    address = models.CharField(max_length=300)
    floor = models.CharField(max_length=20, choices=Floor)
    size = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='vacant')
    is_paid = models.BooleanField(default=False)


RENT_TYPE = (
    ("Monthly", "Monthly"),
    ("Yearly", "Yearly"),
    ("Lease", "Lease")
)

class Rent(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.Model)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rent_type = models.CharField(max_length=20, choices=RENT_TYPE)
    date_paid = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    date_due = models.DateField()
    managed_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, related_name='rents_managed')

    def __str__(self):
        return self.shop.name
    
    

class Rate(models.Model): 

    Floor = [
        ('G', 'Ground Floor'),
        ('1', 'First Floor'),
        ('2', 'Second Floor'),
       
    ]

    STATUS = [
        ('vacant', 'Vacant'),
        ('active', 'Allocated'),
     
       
    ]
     
    no = models.CharField(max_length=5, default=0)
    floor = models.CharField(max_length=20, choices=Floor)
    size = models.IntegerField()
    price = models.ForeignKey(Shop, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='vacant')

    def __str__(self):
        return self.no
    
    @property
    def rent(self):
        return self.size * self.price.price
    
          
    @property
    def shop_price(self):
        result = self.rent * Decimal('1.075')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def shop_rent(self):
        result = self.shop_price * Decimal('1.05')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def shop_charges(self):
        result = self.shop_price * Decimal('0.25')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def shop_agency(self):
        result = self.shop_price * Decimal('0.05')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def shop_legal(self):
        result = self.shop_price * Decimal('0.05')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @property
    def shop_newcharges(self):
        return round(self.shop_agency + self.shop_legal, 2)
    
    @property
    def new_rent(self):
        return round(self.shop_rent + self.shop_newcharges + self.shop_charges, 2)
    
    @property
    def renewal_rent(self):
        return round(self.shop_rent + self.shop_charges, 2)

