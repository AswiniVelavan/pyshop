from sys import modules

from django.db import models
from django.db.models import CharField


class Product(models.Model):
    UNIT_CHOICES = [('lb', 'per lb'), ('each', 'each')]
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='each')


    def formatted_price(self):
        return f"${self.price:.2f}"

    def __str__(self):
        return f"{self.name} - {self.formatted_price()} ({self.get_unit_display()})"



class Offer(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    discount = models.FloatField()
