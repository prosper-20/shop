# Generated by Django 5.0.6 on 2024-05-25 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.CharField(default='', max_length=225),
        ),
    ]