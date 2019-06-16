from django.contrib import admin
from .models import *
admin.site.register([AppUser, UserData, Events, Donation, RegisteredEvents])
# Register your models here.


