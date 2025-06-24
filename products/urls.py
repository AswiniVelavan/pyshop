from pyshop.urls import path
from . import views

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='home'),
    path('new', views.new, name='new'),
    path('login/', views.login_view, name='login'),  # Add this line
    path('signup/', views.signup_view, name='signup'),  # Add this line
    path('accounts/profile/', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
]
