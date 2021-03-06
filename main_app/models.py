from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from django_countries.fields import CountryField

# Create your models here.
LOCATION_CHOICES = (
    # ("Cheydinhal", "Cheydinhal"),
    ("Dawnstar", "Dawnstar"),
    # ("Eletania", "Eletania"),
    ("Falkreath", "Falkreath"),
    # ("Kakariko", "Kakariko"),
    ("Markarth", "Markarth"),
    ("Morthal", "Morthal"),
    # ("Novigrad", "Novigrad"),
    # ("Rapture", "Rapture"),
    ("Riften", "Riften"),
    ("Solitude", "Solitude"),
    # ("Tython", "Tython"),
    ("Whiterun", "Whiterun"),
    ("Winterhold", "Winterhold"),
    ("Windhelm", "Windhelm"),
)

CATEGORY_CHOICES = (
    ("Armor", "Armor"),
    ("Books", "Books"),
    ("Food", "Food"),
    ("Jewelery", "Jewelery"),
    ("Potions", "Potions"),
    ("Weapons", "Weapons"),
)

AVATAR_CHOICES = (
    ("Altmer", "Altmer"),
    ("Argonian", "Argonian"),
    ("Bosmer", "Bosmer"),
    # ("Bounty Hunter", "Bounty Hunter"),
    ("Breton", "Breton"),
    ("Dunmer", "Dunmer"),
    # ("Hylian", "Hylian"),
    ("Imperial", "Imperial"),
    ("Khajiit", "Khajiit"),
    # ("Mandalorian", "Mandalorian"),
    # ("N7", "N7"),
    ("Nord", "Nord"),
    ("Orsimer", "Orsimer"),
    ("Redguard", "Redguard"),
    # ("Spartan", "Spartan"),
    ("...", "..."),
)

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices = CATEGORY_CHOICES)
    weight = models.FloatField(default=1)
    cost = models.FloatField(default=1)
    quantity = models.IntegerField(default=99)
    description = models.TextField()
    img = models.CharField(max_length=500)
    added_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={
            "pk" : self.pk
        })

    def get_put_in_cart_url(self) :
        return reverse("put-in-cart", kwargs={
            "pk" : self.pk
        })

    def get_takeout_from_cart_url(self) :
        return reverse("takeout-from-cart", kwargs={
            "pk" : self.pk
        })

    def get_add_item_url(self) :
        return reverse("add-item", kwargs={
            "pk" : self.pk
        })

    def get_subtract_item_url(self) :
        return reverse("subtract-item", kwargs={
            "pk" : self.pk
        })

    class Meta:
        ordering = ['name']

# extends the default user without having to create a new User model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, choices = LOCATION_CHOICES)   
    avatar = models.CharField(max_length=50, choices = AVATAR_CHOICES)
    # bag = models.ManyToManyField(Product, through='Cart', through_fields=('profile', 'product'))

    def __str__(self):
        return self.user.username

class OrderItem(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True, null=True)

    def get_item_total(self):
        return self.item.cost *self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

class Order(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_order_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_item_total()
        return total
    
class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# class Payment(models.Model):
#     stripe_id = models.CharField(max_length=50)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, 
#                              on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username