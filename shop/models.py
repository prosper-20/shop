from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum
from customer.models import Customer


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

    APPROVAL_STATUS = (
        ('In review', 'In review'),
        ('Pending Approval', 'Pending Approval'),
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    no = models.CharField(max_length=5, unique=True)
    address = models.CharField(max_length=300)
    floor = models.CharField(max_length=20, choices=Floor)
    size = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='vacant')
    is_paid = models.BooleanField(default=False)
    approval = models.CharField(max_length=100, choices=APPROVAL_STATUS)

    def __str__(self):
        return f"Shop {self.no}"
    
    @staticmethod
    def allocated_shops_count():
        return Shop.objects.filter(status="allocated").count()
    
    @staticmethod
    def expected_rent_fees():
        allocated_shops_sum = Shop.objects.filter(status='allocated').aggregate(total_sum=Sum('price'))['total_sum'] or 0
        formatted_sum = formatted_sum = '{:.2f}'.format(allocated_shops_sum)
        return formatted_sum
    
    @staticmethod
    def total_paid_shops_price():
        total_paid_price = Shop.objects.filter(is_paid=True).aggregate(Sum('price'))['price__sum'] or 0.0
        formatted_sum = formatted_sum = '{:.2f}'.format(total_paid_price)
        return formatted_sum

RENT_TYPE = (
    ("Monthly", "Monthly"),
    ("Yearly", "Yearly"),
    ("Lease", "Lease")
)

class Rent(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.Model)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rent_type = models.CharField(max_length=20, choices=RENT_TYPE)
    date_paid = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)  # New field
    date_due = models.DateField()

    def __str__(self):
        return self.shop.name
    
    @property
    def is_due(self):
        today = timezone.now().date()
        return today > self.date_due
    
    def total_paid_rents(self):
        total_paid_rents = Rent.objects.filter(
            shop=self,  # Filter by the current shop instance
            is_paid=True  # Only consider rents that have been paid
        ).aggregate(Sum('rent_amount'))['rent_amount__sum'] or 0.0

        return total_paid_rents

    @staticmethod
    def rents_due_count():
        today = timezone.now().date()
        return Rent.objects.filter(date_due__lt=today).count()
    
    @staticmethod
    def rents_paid_count():
        return Rent.objects.filter(is_paid=True).count()
    
   
    
    

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
    



# 32,000.00
# 29,000.00
# 28,000.00
# 25,000.00
# 22,000.00
# 19,000.00

