# Generated by Django 4.2.13 on 2024-07-19 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_rent_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]