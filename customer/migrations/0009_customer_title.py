# Generated by Django 4.2.13 on 2024-08-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0008_customer_is_reviewed"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="title",
            field=models.CharField(
                choices=[("Mr", "Mr"), ("Mrs", "Mrs"), ("Miss", "Miss")],
                default="Mr",
                max_length=10,
            ),
        ),
    ]
