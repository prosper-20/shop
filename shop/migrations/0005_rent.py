# Generated by Django 4.2.13 on 2024-07-10 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0004_shop_is_paid_shop_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent_type', models.CharField(choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly'), ('Lease', 'Lease')], max_length=20)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('date_due', models.DateField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(on_delete=models.Model, to='shop.shop')),
            ],
        ),
    ]