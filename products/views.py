from itertools import product
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import CartItem, Order, OrderItem, Product
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem


# Index View (Product Listing)
def index(request):
    products = Product.objects.all()

    return render(request, 'products/index.html', {'products': products})


# New Products View (Can be updated as per your requirement)
def new(request):
    return HttpResponse('New Products')


# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def profile(request):
    return render(request, 'registration/profile.html')


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'products/cart.html', {'items': items, 'total': total})


@login_required
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('cart')

    with transaction.atomic():
        # Create the order
        order = Order.objects.create(user=user)

        for item in cart_items:
            product = item.product

            # Check if enough stock is available
            if product.stock >= item.quantity:
                # Create an OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity
                )

                # Reduce stock
                product.stock -= item.quantity
                product.save()
            else:
                return render(request, 'products/checkout_error.html', {
                    'message': f"Not enough stock for {product.name}."
                })

        # Clear the cart after order is placed
        cart_items.delete()

    return render(request, 'products/checkout_success.html', {'order': order})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity', 1)

    try:
        quantity = Decimal(quantity)
    except:
        quantity = 1

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('cart')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')
