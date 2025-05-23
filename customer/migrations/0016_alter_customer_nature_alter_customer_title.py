# Generated by Django 4.2.13 on 2025-05-21 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0015_alter_customer_email_alter_customer_nature_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="nature",
            field=models.CharField(
                choices=[
                    ("Supermarket", "Supermarket"),
                    ("Bridal Wears", "Bridal Wears"),
                    ("Laundry", "Laundry"),
                    ("Pharmacy", "Pharmacy"),
                    ("Car Dealer", "Car Dealer"),
                    ("Courier/Dispatch", "Courier/Dispatch"),
                    ("Banking/Insurance", "Banking/Insurance"),
                    ("Barbing/Salon", "Barbing/Salon"),
                    ("Restaurant", "Restaurant"),
                    ("Legal Aid Services", "Legal Aid Services"),
                    ("Food and Drinks", "Food and Drinks"),
                    ("Makeup Artist", "Makeup Artist"),
                    ("Building", "Building"),
                    ("Tailoring", "Tailoring"),
                    ("Studio", "Studio"),
                    ("Beauty Salon", "Beauty Salon"),
                    ("Bakery", "Bakery"),
                    ("Wine Seller", "Wine Seller"),
                    ("Logistics", "Logistics"),
                    ("Clothing", "Clothing"),
                    ("Fabrics", "Fabrics"),
                    ("Oriflame Dealer", "Oriflame Dealer"),
                    ("Fruit Seller", "Fruit Seller"),
                    ("Communication", "Communication"),
                    ("Business Centre", "Business Centre"),
                    ("Bank", "Bank"),
                    ("Tv Repair", "Tv Repair"),
                    ("Hair Business", "Hair Business"),
                    ("Consultancy", "Consultancy"),
                    ("Skin Beauty Store", "Skin Beauty Store"),
                    ("Dispatch Office", "Dispatch Office"),
                    ("Atm Customization", "Atm Customization"),
                    ("Loan Business", "Loan Business"),
                    ("Children Wears", "Children Wears"),
                    ("Electrical/Electronics Store", "Electrical/Electronics Store"),
                    ("Home Wears Store", "Home Wears Store"),
                    ("Travel Agency", "Travel Agency"),
                    ("Photo Studio", "Photo Studio"),
                    ("Real Estate", "Real Estate"),
                    ("Law Firm", "Law Firm"),
                    ("Graphic Design and Branding", "Graphic Design and Branding"),
                    ("Perfumery", "Perfumery"),
                    ("NGO", "NGO"),
                    ("Branding Business", "Branding Business"),
                    ("Pastries & Cake", "Pastries & Cakes"),
                    ("Mtn Service Provider Business", "Mtn Service Provider Business"),
                    ("Cyber Cafe", "Cyber Cafe"),
                    ("Wood Floor Trader", "Wood Floor Trader"),
                    ("Others", "Others"),
                ],
                default="",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="title",
            field=models.CharField(
                choices=[
                    ("Mr", "Mr"),
                    ("Mrs", "Mrs"),
                    ("Miss", "Miss"),
                    ("Engr.", "Engr."),
                    ("Dr.", "Dr."),
                    ("Miss", "Miss"),
                ],
                default="Mr",
                max_length=10,
            ),
        ),
    ]
