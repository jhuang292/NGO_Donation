from django.contrib import admin
from .models import *
admin.site.register([CustomUser,UserData,  Events, Donation, RegisteredEvents])

# Register your models here.


