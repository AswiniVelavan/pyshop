from pyshop.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('new', views.new, name='new'),
    path('login/', views.login_view, name='login'),  # Add this line
    path('signup/', views.signup_view, name='signup'),  # Add this line
]
