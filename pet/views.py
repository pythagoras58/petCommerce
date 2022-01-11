"""
    This class file determines what is rendered on all the html (template)
    pages.
"""
# import messages
from django.contrib import messages
# registration of user
from django.contrib.auth.models import User, auth
# sending email
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
# timezone
from django.utils import timezone
# use class based views
from django.views.generic import ListView, DetailView

# import all models
from .models import Item, OrderItem, Order


# class views for the Home Page (index page)
class HomeView(ListView):
    model = Item
    template_name = "home.html"


# when a product is selected it is redirected to this page for further processing
class ProductDetailView(DetailView):
    model = Item
    template_name = "product.html"


# login view
def userLogin(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # verify the user
        user = auth.authenticate(
            username=username,
            password=password
        )

        """
            check if the user is registered in the database
            then make a redirect to the desired pages
            
            :: could have used:
            username = request.POST['username']
            password = request.POST['password']
            But depreciated and shows valueError
        """

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "User Credentials Not Correct")

    else:
        return render(request, "login.html")

# log the user out
def logout(request):
    """
    To logout the user::the user data should be cleared of the cache
    :param request:
    :return: the index page
    """
    auth.logout(request)
    return redirect('/')


# check out cart view.
def checkout(request):
    return render(request, "checkout.html")


# registration view
def register(request):
    # register the user
    if request.method == "POST":
        # get all the data from the form submitted by the user
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        email = request.POST.get('email')
        """
        lastname = request.POST['lastname']
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        email = request.POST['email']
        """

        email_user = User.objects.filter(email=email).first()
        user_check = User.objects.filter(username=username).filter()

        # validate password
        if password != confirmpassword:
            messages.warning(request, "Sorry!! Passwords Mismatch")
            return redirect('register')

        # if user_check:
        # messages.warning(request, "Sorry!! Username already used")

        # validate email
        if email_user:
            messages.warning(request, "Sorry!! Email already used")
            return redirect('register')

        # create the new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=firstname,
            last_name=lastname
        )

        # push the user
        user.save()
        messages.success(request, "Details Created")
        # redirect to home page
        return redirect('/')


    else:
        return render(request, "register.html")


# contact page view
def contact(request):
    if request.method == "POST":
        # get the data from the form on the contact page
        message_name = request.POST['message_name']
        message_email = request.POST['message_email']
        user_message = request.POST.get('user_message', False)  # to prevent multivalued key exception
        congratulations_message = " Email received"

        # send email when the contact form is submitted
        send_mail(
            'Pet Shop Message From ' + message_name,  # subject
            user_message,  # message
            message_email,  # from email
            ['solomondanso58@gmail.com'],
            fail_silently=True  # to email
        )
        # proceed to make changes to the settings.py file

        # refer user to the same page
        return render(request, "contact.html", {'congratulations_message': message_name + congratulations_message})
    else:
        return render(request, "contact.html")


"""
 add_to_cart :: This function is to allow products addition to the cart by the user
 it ensures the implementation of foreign key constraint that has been set in the model 
 files
"""


def add_to_cart(request, slug):
    # get the items
    item = get_object_or_404(Item, slug=slug)
    # assign the item
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    # get order query set
    order_query_set = Order.objects.filter(user=request.user, ordered=False)

    # check if the order query set exist
    if order_query_set.exists():
        # get the first item of the query set
        order = order_query_set[0]

        # check the filter
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item.title}'s quantity was updated")
            return redirect('ProductDetailView', slug=slug)

        else:
            # add the order item to the order
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item.title}'s was added to the cart")
            return redirect('ProductDetailView', slug=slug)


    else:
        # create the order on the spot if there is no order query set
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered=False, ordered_date=ordered_date)
        order.items.add(order_item)  # due to it been a many to many field
        order.save()
        messages.success(request, f"{item.title}'s was added to the cart")
        return redirect('ProductDetailView', slug=slug)


"""
Function to help remove items that has been added
to the cart by the users
"""


def remove_from_cart(request, slug):
    # get the items
    item = get_object_or_404(Item, slug=slug)
    # assign the item
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    # get order query set
    order_query_set = Order.objects.filter(user=request.user, ordered=False)

    # check if the order query set exist
    if order_query_set.exists():
        # get the first item of the query set
        order = order_query_set[0]

        # check the filter
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            # save the item
            order.save()
            messages.success(request, f"{item.title} was removed from cart")
            return redirect('ProductDetailView', slug=slug)

        else:
            messages.info(request, f"{item.title} not in cart")
            return redirect('ProductDetailView', slug=slug)

    else:
        messages.info(request, "You have no active orders in cart")
        return redirect('ProductDetailView', slug=slug)
