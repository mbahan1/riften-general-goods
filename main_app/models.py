from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    # ("Furniture", "Furniture"),
    ("Jewelery", "Jewelery"),
    ("Materials", "Materials"),
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
    quantity = models.IntegerField(default=1)
    description = models.TextField()
    img = models.CharField(max_length=500)
    added_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# extends the default user without having to create a new User model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, choices = LOCATION_CHOICES)   
    avatar = models.CharField(max_length=50, choices = AVATAR_CHOICES)
    bag = models.ManyToManyField(Product, through='Cart', through_fields=('profile', 'product'))

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    equiped = models.BooleanField(default=False)

    def __str__(self):
        return (self.profile.user.username+":"+self.product.name)
