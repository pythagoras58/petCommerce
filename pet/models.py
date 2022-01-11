from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# CHOICES as turples :: This is the categories of products available
CATEGORY_CHOICES = (
    ('Pet Product', 'Pet Product'),
    ('Pet', 'Pet')
)

# CHOICE AS TURPLES :: This is the Product Selling Tag
LABEL_CHOICES = (
    ('S', 'secondary'),
    ('P', 'primary'),
    ('D', 'danger'),
)

# Create your models here.

"""
    The Item models holds the details of all Items
    available in the online store front
"""


class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    categories = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    labels = models.CharField(max_length=10, choices=LABEL_CHOICES)
    image = models.ImageField(default='default.jpg', upload_to='static/image')
    slug = models.SlugField()

    def __str__(self):
        return self.title

    # specify add to cart
    def get_add_to_cart_url(self):
        return reverse('add-to-cart', kwargs={'slug': self.slug})

    # specify remove from cart
    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={'slug': self.slug})


"""
    The Details of Items that have been ordered
    From the store front
"""


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


"""
    Model for variations :: 
    Pet variations
"""

"""
this class is to handle pet variation suggestions on the store site
"""
class Variation(models.Model):
    # variations must be linked to a certain item
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    # make the item unique with the name
    class Meta:
        unique_together = (
            ('item', 'name')
        )

    # define string method
    def __str__(self):
        return self.name


"""
itemvariation class links all variations items to the variation class
it holds the value and the url to the variatioitem
"""
class ItemVariation(models.Model):
    # variations item must be linked to a variation
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    attachment = models.ImageField(upload_to="static/image")

    # make the variation unique with the value
    class Meta:
        unique_together = (
            ('variation', 'value')
        )

    # define string method
    def __str__(self):
        return self.value


"""
    The details of the Order
    :: About the user, and when the order was placed
"""


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username
