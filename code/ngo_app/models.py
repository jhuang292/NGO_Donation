from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager , AbstractUser
from django.contrib.auth.models import Group, Permission ,User
from phone_field import PhoneField
from datetime import date

from django.contrib.auth import get_user_model


# Create your models here.

class EventRegistration(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    cma = models.IntegerField()
    phone = PhoneField(help_text="Contact Number")
    email = models.EmailField()
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=100)
    state_code = models.CharField(max_length=2)
    zip = models.CharField(max_length=8)
    country = models.CharField(max_length=30)
    urbanization = models.CharField(max_length=30)
    user_user_model = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=None)


class Events(models.Model):
    name = models.CharField(max_length=40)
    type = models.CharField(max_length=30)
    status = models.CharField(max_length=10, default='Active')

    def __str__(self):
        return str(self.name)


class Donation(models.Model):
    event = models.ForeignKey(Events, on_delete= models.CASCADE)
    donation_amount = models.DecimalField(decimal_places=2, max_digits= 1000000000000000)
    user_data = models.ForeignKey(EventRegistration, on_delete= models.CASCADE)
    is_recurring = models.BooleanField(default=False)
    date_dj_name = models.DateField(null=True, default=date.today())
    is_paid = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user_data)


class AdminToUserMAp(models.Model):
    Admin = models.ForeignKey(User , on_delete=models.CASCADE, null=False, related_name='admin')
    Non_Admin = models.ForeignKey(User , on_delete=models.CASCADE, null=False, related_name = 'non_admin')


class AdminToEventMap(models.Model):
    Admin = models.ForeignKey(User , on_delete=models.CASCADE, null=False)
    event = models.ForeignKey(Events , on_delete=models.CASCADE, null=False)






