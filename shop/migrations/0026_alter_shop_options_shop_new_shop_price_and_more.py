# Generated by Django 4.2.13 on 2024-10-02 21:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0025_paymentslip_narration_alter_income_date_created"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shop",
            options={"ordering": ["no"]},
        ),
        migrations.AddField(
            model_name="shop",
            name="new_shop_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="income",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 10, 2, 21, 5, 57, 721969, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
