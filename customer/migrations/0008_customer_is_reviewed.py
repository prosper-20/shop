# Generated by Django 4.2.13 on 2024-08-05 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0007_customer_approval_officer_note_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="is_reviewed",
            field=models.CharField(
                choices=[
                    ("Is Reviewed", "Is Reviewed"),
                    ("Not Reviewed", "Not Reviewed"),
                ],
                default="Not Reviewed",
                max_length=100,
            ),
        ),
    ]
