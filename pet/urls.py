"""
This class file handles the list of all url paths in the
application with their proper redirection
"""

from django.urls import path

from .views import (
    HomeView,
    ProductDetailView,
    checkout,
    contact,
    add_to_cart,
    remove_from_cart,
    register,
    userLogin,
    logout,
)

urlpatterns = [
    path('', HomeView.as_view(), name="HomeView"),  # Home page
    path('contact/', contact, name="contact"),  # contact page
    path('userLogin/', userLogin, name="userLogin"),  # login page
    path('logout/', logout, name="logout"),  # logout page
    path('register/', register, name="register"),  # customer registration page
    path('add-to-cart/<slug>/', add_to_cart, name="add-to-cart"), # to to cart path
    path('remove-from-cart/<slug>/', remove_from_cart, name="remove-from-cart"), # remove from cart path
    path('product/<slug>/', ProductDetailView.as_view(), name="ProductDetailView"),  # product page path
    path('checkout/', checkout, name="checkout"),  # checkout page
]
