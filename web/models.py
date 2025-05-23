from django.db import models


class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.full_name


class ShopType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# class Shop(models.Model):
#     name = models.CharField(max_length=255)
#     address = models.CharField(max_length=255)
#     shop_type = models.C
