from django.forms import ModelForm
from .models import UserData

class UserDataForms(ModelForm):
    class Meta:
        model = UserData
        fields = ["first_name","last_name", "address_line1", "address_line2", "city", "state_code", "country"]
