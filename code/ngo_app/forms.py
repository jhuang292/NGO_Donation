from django.forms import ModelForm
from .models import EventRegistration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User ,Group
from django import forms
from django.shortcuts import get_object_or_404

class UserDataForms(ModelForm):
    #def __init__(self,data):
        #self.cleaned_data = None
        #super().__init__(data=data)
    class Meta:
        model = EventRegistration
        fields = ['first_name','last_name','cma', 'phone','email', 'address_line1','address_line2', 'city','state_code',  'zip',  'country', 'urbanization']





class AddUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    email = forms.EmailField()

    class Meta:
        model = User
        fields =['first_name','last_name','email', 'username',"password1", "password2"]


    # def save(self, commit=True):
    #     user = super(AddUserForm, self).save(commit=True)
    #     self.instance.groups.set(get_object_or_404(Group, pk=1))
    #     user.save()
    #     user.email = self.cleaned_data["email"]
    #     user.first_name = self.changed_data['first_name']
    #     user.last_name = self.changed_data['last_name']
    #
    #     if commit:
    #         user.save()
    #     return user


