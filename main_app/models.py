from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
LOCATION_CHOICES = (

)

CATEGORY_CHOICES = (

)

AVATAR_CHOICES = (

)

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     category = models.CharField(max_length=50, choices = CATEGORY_CHOICES)
#     weight = models.IntegerField(default=1)
#     cost = models.IntegerField(default=1)
#     quantity = models.IntegerField(default=1)
#     description = models.TextField()
#     img = models.CharField(max_length=500)
#     added_on = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ['name']

# # extends the default user without having to create a new User model
# class Profile(models.Model):
#     user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
#     location = models.CharField(max_length=50, choices = LOCATION_CHOICES)   
#     avatar = models.CharField(max_length=50, choices = AVATAR_CHOICES)
#     bag = models.ManyToManyField(Product, through='Cart', through_fields=('profile', 'product'))

#     def __str__(self):
#         return self.user.username

# class Cart(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     count = models.IntegerField(default=1)
#     equiped = models.BooleanField(default=False)

#     def __str__(self):
#         return (self.profile.user.username+":"+self.product.name)