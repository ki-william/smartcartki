from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
import random
from django.utils.encoding import smart_str

class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    Quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products")
    barcode = models.CharField(max_length=256, blank=True, null=False)
    weight = models.DecimalField(max_digits=7, decimal_places=2,default=0)

    def __str__(self):
        return self.name
 

class UserProfile(AbstractUser):
    image = models.ImageField(upload_to="users",
                              blank=True)
    balance = models.DecimalField(default=10000,
                                  max_digits=99,
                                  decimal_places=3)


class Cart(models.Model):
    cartnumber = models.IntegerField(default=0, null=True, blank=True)
    barcode = models.CharField(max_length=256, blank=True, null=True)
    isreserved = models.BooleanField(default=False)
    currentuser = models.ForeignKey(UserProfile,
                                on_delete=models.CASCADE,
                                related_name="UserProfile", null=True)

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True,null=True)
    total_price= models.IntegerField(default=0,null=True,blank=True)


    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="product", null=True)
    order = models.ForeignKey(Order, related_name="orderItems",
                              on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0, null=True, blank=True)


rates = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
    )
class Rate (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)   
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)
    rate = models.IntegerField(choices=rates, max_length= 50, default=1)


####
#class Vcart(models.Model):
#    vcartid = models.IntegerField(default=0, null=True, blank=True)
#    user = models.ForeignKey(Product, on_delete=models.CASCADE,
#                                related_name="UserProfile", null=True)
#    cart = models.ForeignKey(Cart,
#                             on_delete=models.CASCADE,
#                             null=True,
#                             blank=True)
#
####
#    order = models.ForeignKey(Order, related_name="orderItems",
#                              on_delete=models.SET_NULL,null=True)
#    date_added = models.DateTimeField(auto_now_add=True)

####





@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
