# Generated by Django 4.2.13 on 2024-07-19 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_alter_customer_nextdue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='exitdate',
            field=models.DateField(blank=True, null=True),
        ),
    ]