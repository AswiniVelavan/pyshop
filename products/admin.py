from django.contrib import admin
from .models import Product, Offer, CartItem, Order, OrderItem

class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'unit')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('user', 'product')
    search_fields = ('user__username', 'product__name')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')

admin.site.register(Product, ProductAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)




