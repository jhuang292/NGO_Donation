from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
admin.site.register([EventRegistration, Donation, Events ,AdminToEventMap , AdminToUserMAp])




