from django.db import models
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum
from customer.models import Customer
from django.core.validators import MinLengthValidator
from django.db.models import Sum
from django.core.exceptions import ValidationError
from datetime import timedelta

User = get_user_model()

class Shop(models.Model):
 
    Type = [
        ('Platinum', 'Platinum'),
        ('Titanium', 'Titanium'),
        ('Diamond', 'Diamond'),
        ('Premium', 'Premium'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),

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

    


    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_shop_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    caution_fee = models.DecimalField(max_digits=12, decimal_places=2, default=100000.00)
    no = models.CharField(max_length=5, validators=[MinLengthValidator(4)], unique=True)
    address = models.CharField(max_length=300)
    floor = models.CharField(max_length=20, choices=Floor)
    size = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='vacant')
    is_paid = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Shop {self.no}"
    
    class Meta:
        ordering = ["no"]
    
    # @staticmethod
    # def allocated_shops_count():
    #     return Shop.objects.filter(status="allocated").count()

    @staticmethod
    def allocated_shops_count():
        return Rent.objects.filter(is_paid=True, is_expired=False).count()
    
    # @staticmethod
    # def expected_rent_fees():
    #     allocated_shops_sum = Shop.objects.filter(status='allocated').aggregate(total_sum=Sum('price'))['total_sum'] or 0
    #     formatted_sum = formatted_sum = '{:.2f}'.format(allocated_shops_sum)
    #     return formatted_sum


    @staticmethod
    def expected_rent_fees():
        """
        Returns the sum of new_total_rent_payable for allocated shops
        in the same format as your example (formatted string)
        """
        from decimal import Decimal
        
        # Initialize total
        total = Decimal('0.00')
        
        # Calculate sum for allocated shops
        for shop in Shop.objects.filter(status='allocated'):
            total += Decimal(str(shop.new_total_rent_payable))
        
        # Format to 2 decimal places
        return '{:.2f}'.format(total)
    
    @staticmethod
    def total_paid_shops_price():
        total_paid_price = Shop.objects.filter(is_paid=True).aggregate(Sum('price'))['price__sum'] or 0.0
        formatted_sum = formatted_sum = '{:.2f}'.format(total_paid_price)
        return formatted_sum
    
    # YOU ADDED THIS FORM THE RATE MODEL
    
    @property
    def rent(self):
        return self.size * self.price
    
    # @property
    # def new_rent(self):
    #     return self.new_shop_price * self.size
    
    @property
    def vat(self): # 7.5% OF THE RENT
        result = self.rent * Decimal('0.075')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # return round(0.0075 * self.rent, 2)
    
    @property
    def wht(self):  # 5% 
        result = self.rent * Decimal(0.05)
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def annual_rent(self):
        result = self.rent + self.vat
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def gross_rent(self):
        return round(self.rent + self.vat + self.wht, 2)
    
    @property
    def new_shop_agency(self):
        result = (self.rent + self.vat) * Decimal('0.15')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def new_shop_legal(self):
        result = (self.rent + self.vat) * Decimal('0.05')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def new_service_charge(self):
        result = (self.rent + self.vat) * Decimal('0.25')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    
    @property
    def new_total_rent_payable(self):
        return round(self.rent + self.new_shop_agency + self.new_shop_legal + self.new_service_charge + self.wht + self.vat + self.caution_fee, 2)
    
    @property
    def renewal_rent_payable(self):
        return round(self.rent + self.new_service_charge)
          
    @property
    def shop_price(self):
        result = self.rent * Decimal('1.075')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def shop_rent(self): # FOR OLD CUSTOMERS
        result = self.shop_price * Decimal('1.05')
        return result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property # you just added these
    def new_shop_rent(self): # FOR NEW CUSTOMERS
        if self.new_shop_price:
            result = self.new_rent * Decimal('1.05')
        result = 0
        return result.quantize
    
    
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
    def old_customer_total_rent_payable(self):
        return round(self.gross_rent + self.new_service_charge, 2)
    # @property
    # def new_rent(self):
    #     return round(self.shop_rent + self.shop_newcharges + self.shop_charges, 2)
    
    @property
    def renewal_rent(self):
        return round(self.gross_rent + self.shop_charges, 2)
    
    @property
    def total(self):
        # Calculate the total as the sum of specific properties
        return round(self.rent + self.shop_price + self.shop_rent +
                     self.shop_charges + self.shop_agency + self.shop_legal, 2)
    

    

RENT_TYPE = (
    ("Monthly", "Monthly"),
    ("Yearly", "Yearly"),
    ("Lease", "Lease"),
    ("1 year", "1 year"),
    ("2 year(s)", "2 years(s)"),
    ("5 years", "5 years")
)

class Rent(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rent_type = models.CharField(max_length=20, choices=RENT_TYPE)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    date_paid = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)  # New field
    rent_start = models.DateField(default=timezone.now)
    date_due = models.DateField()
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.shop.name

    
    @property
    def is_due(self):
        today = timezone.now().date()
        return today > self.date_due
    
    # def total_paid_rents(self):
    #     total_paid_rents = Rent.objects.filter(
    #         shop=self,  # Filter by the current shop instance
    #         is_paid=True  # Only consider rents that have been paid
    #     ).aggregate(Sum('rent_amount'))['rent_amount__sum'] or 0.0

    #     return total_paid_rents


    # @staticmethod
    # def total_paid_shops_price():
    #     """
    #     Returns total paid amount for current (non-expired) rentals
    #     """
    #     total_paid = Rent.objects.filter(
    #         is_paid=True,
    #         is_expired=False
    #     ).aggregate(
    #         total_sum=Sum('amount_paid')
    #     )['total_sum'] or Decimal('0.00')
        
    #     return '{:.2f}'.format(total_paid)
    

    # @staticmethod
    # def total_paid_shops_price():
    #     """
    #     Returns the total amount actually paid for all rented shops (from Rent model)
    #     """
    #     from django.db.models import Sum
        
    #     # Sum all amount_paid from Rent records that are marked as paid
    #     total_paid = Rent.objects.filter(is_paid=True).aggregate(
    #         total_sum=Sum('amount_paid')
    #     )['total_sum'] or Decimal('0.00')
        
    #     return '{:.2f}'.format(total_paid)
    

    @staticmethod
    def total_paid_shops_price():
        """
        Returns the sum of new_total_rent_payable for allocated shops
        in the same format as your example (formatted string)
        """
        from decimal import Decimal
        
        # Initialize total
        total = Decimal('0.00')
        
        # Calculate sum for allocated shops
        for rent in Rent.objects.filter(is_paid=True):
            print("rterere", rent.amount_paid)
            total += Decimal(str(rent.amount_paid))
        
        # Format to 2 decimal places
        return '{:.2f}'.format(total)

    @staticmethod
    def rents_due_count():
        today = timezone.now().date()
        return Rent.objects.filter(is_expired=True).count()
        # return Rent.objects.filter(date_due__lt=today).count() THJIS WAS THE OLD COMPUTATION
    
    @staticmethod
    def rents_paid_count():
        return Rent.objects.filter(is_paid=True).count()
    
    # YOU ADDED THIS FORM THE RATE MODEL
    
    @property
    def rent(self):
        return self.shop.size * self.shop.price
    
          
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
    def old_customer_total_rent_payable(self):
        return round(self.shop_rent + self.shop_newcharges, 2)
    
    @property
    def renewal_rent(self):
        return round(self.shop_rent + self.shop_charges, 2)
    
   
    
    

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
    
    
    
    


NAME_CHOICES = (
    ("Nina", "Nina"),
    ("Chairman", "Chariman")
)


class Income(models.Model):
    name = models.CharField(max_length=200, choices=NAME_CHOICES)
    daily = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal("0.00"))
    new_daily = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    weekly = models.DecimalField(max_digits=15, decimal_places=2,  default=Decimal("0.00"))
    new_weekly = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    yearly = models.DecimalField(max_digits=15, decimal_places=2,  default=Decimal("0.00"))
    new_yearly = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    # def save(self, *args, **kwargs):
    #     # Check if new_daily is provided and not None
    #     if self.new_daily is not None:
    #         # Add new_daily to daily
    #         print(self.daily)
    #         print(self.new_daily)
    #         self.daily += self.new_daily
    #         # Reset new_daily after adding to daily
    #         self.new_daily = Decimal('0.00')
    #     elif self.new_weekly is not None:
    #         self.weekly += self.new_weekly
    #         self.new_weekly = Decimal('0.00')
    #     elif self.new_yearly is not None:
    #         self.yearly += self.new_yearly
    #         self.new_yearly = Decimal('0.00')

    #     # Call the parent class's save method
    #     super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    

    @staticmethod
    def total_daily_receipts():
        result = Income.objects.aggregate(total_daily=Sum('daily'))
        return result['total_daily'] or Decimal('0.00')
    
    @staticmethod
    def total_weekly_receipts():
        result = Income.objects.aggregate(total_weekly=Sum('weekly'))
        return result['total_weekly'] or Decimal('0.00')
    
    @staticmethod
    def total_yearly_receipts():
        result = Income.objects.aggregate(total_yearly=Sum('yearly'))
        return result['total_yearly'] or Decimal('0.00')



def validate_image_size(image):
    filesize = image.file.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Maximum file size is {megabyte_limit}MB") 

PAYMENT_ACCOUNT_CHOICES = [
        ('Nina Sky', 'Nina Sky'),
        ('Chairman', 'Chairman'),
    ]


class PaymentSlip(models.Model):
    PAYMENT_ACCOUNT_CHOICES = [
        ('Nina Sky', 'Nina Sky'),
        ('Chairman', 'Chairman'),
    ]

    REVIEW_CHOICES =(
        ("Reviewed", "Reviewed"),
        ("Mot Reviewed", "Not Reviewed")
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_account = models.CharField(choices=PAYMENT_ACCOUNT_CHOICES, max_length=30)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    shop_no = models.ForeignKey(Shop, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="payment_receipts", blank=True, null=True, validators=[validate_image_size])
    payment_date = models.DateField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    narration = models.CharField(max_length=255, blank=True, null=True)
    is_reviewed = models.CharField(choices=REVIEW_CHOICES, max_length=100)
    is_verified = models.BooleanField(default=False)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.customer.name



# 32,000.00
# 29,000.00
# 28,000.00
# 25,000.00
# 22,000.00
# 19,000.00

