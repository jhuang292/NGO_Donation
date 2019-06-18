from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager , AbstractUser
from django.contrib.auth.models import Group, Permission ,User
from phone_field import PhoneField


from django.contrib.auth import get_user_model


# Create your models here.

class EventRegistration(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    cma = models.IntegerField(max_length=13)
    phone = PhoneField(help_text="Contact Number")
    email = models.EmailField()
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=100)
    state_code = models.CharField(max_length=2)
    zip = models.CharField(max_length=8)
    country = models.CharField(max_length=30)
    urbanization =models.CharField(max_length=30)



class Events(models.Model):
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    status = models.CharField(max_length=10)


class Donation(models.Model):
    event = models.ForeignKey(Events, on_delete= models.CASCADE)
    donation_amount = models.DecimalField(decimal_places=2, max_digits= 1000000000000000)
    user_data = models.ForeignKey(EventRegistration, on_delete= models.CASCADE)


class RegisteredEvents(models.Model):
    doner = models.ForeignKey(EventRegistration, on_delete= models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.PROTECT)
    user_model_user = models.ForeignKey(User, on_delete=models.PROTECT)










