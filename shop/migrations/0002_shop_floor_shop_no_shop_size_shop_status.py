# Generated by Django 4.2.13 on 2024-07-07 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='floor',
            field=models.CharField(choices=[('G', 'Ground Floor'), ('1', 'First Floor'), ('2', 'Second Floor')], default='Ground Floor', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='no',
            field=models.CharField(default=0, max_length=5),
        ),
        migrations.AddField(
            model_name='shop',
            name='size',
            field=models.IntegerField(default=600),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='status',
            field=models.CharField(choices=[('vacant', 'Vacant'), ('allocated', 'Allocated')], default='vacant', max_length=10),
        ),
    ]