from django.contrib import admin
from .models import *
admin.site.register([AppUser, UserData, Donation, Events,RegisteredEvents])
# Register your models here.
