# Generated by Django 4.2.13 on 2024-07-19 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0002_alter_customer_no_alter_customer_phone_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="exitdate",
            field=models.DateField(default="2023-10-21"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="customer",
            name="nextdue",
            field=models.DateField(default="2021-02-12"),
            preserve_default=False,
        ),
    ]
