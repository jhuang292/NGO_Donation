from django.db import models
from django.contrib.auth import models
from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from  django.contrib.auth.models import PermissionsMixin


# Create your models here


class AppUser(Model):
    first_name = models.CharField(max_length=10, blank=False, default='', name="First Name")
    last_name = models.CharField(max_length=10, blank=False, default='', name="Last Name")
    email = models.EmailField(blank=False, default='')
    group = models.ForeignKey(Group, on_delete=models.PROTECT, default="User")



class UserData(Model):
    first_name = models.CharField(max_length=40)
    Last_name = models.CharField(max_length=40)
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state_code = models.CharField(max_length=2)
    zip = models.CharField(max_length=8)
    coutry = models.CharField(max_length=30)


class Events(Model):
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    status = models.CharField(max_length=10)


class Donation(Model):
    event = models.ForeignKey(Events, on_delete= models.CASCADE)
    donation_amount = models.DecimalField(decimal_places=2, max_digits= 1000000000000000)
    user_data = models.ForeignKey(UserData, on_delete= models.CASCADE)


class RegisteredEvents(Model):
    event = models.ForeignKey(Events, on_delete= models.CASCADE)
    custom_user = models.ForeignKey(AppUser, on_delete= models.CASCADE)


