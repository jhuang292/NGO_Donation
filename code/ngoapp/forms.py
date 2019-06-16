from django.db import models
from django.forms import ModelForm
from .models import AppUser

class AuthorForm(ModelForm):
    class Meta:
        model = AppUser
        fields = ['name', 'title', 'birth_date']