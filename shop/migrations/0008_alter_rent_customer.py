# Generated by Django 4.2.13 on 2024-07-19 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_alter_customer_exitdate'),
        ('shop', '0007_alter_rent_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='customer',
            field=models.ForeignKey(limit_choices_to={'is_staff': False}, on_delete=django.db.models.deletion.CASCADE, to='customer.customer'),
        ),
    ]