# Generated by Django 4.2.13 on 2024-10-10 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0027_remove_shop_new_shop_price_alter_income_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='new_shop_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='income',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 10, 17, 12, 1, 769993, tzinfo=datetime.timezone.utc)),
        ),
    ]