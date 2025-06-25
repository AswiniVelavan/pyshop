from sys import modules

from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField
from decimal import Decimal, ROUND_HALF_UP


class Product(models.Model):
    UNIT_CHOICES = [('lb', 'per lb'), ('each', 'each')]
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.CharField(max_length=2083)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='each')

    def formatted_price(self):
        return f"${self.price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"

    def __str__(self):
        return f"{self.name} - {self.formatted_price()} ({self.get_unit_display()})"


class Offer(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1)

    def total_price(self):
        total = self.product.price * self.quantity
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def formatted_total_price(self):
        return f"${self.total_price()}"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
