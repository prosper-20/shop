# Generated by Django 4.2.13 on 2024-07-30 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_remove_shop_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='shop',
            name='no',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]