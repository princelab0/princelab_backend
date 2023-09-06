#create forms.py.
#importing the models from core modules and import django forms.
from core.models import User
from django import forms

class sign_In(forms.ModelForm):
    class Meta:
        model=User
        feild="__all__"
#importing all the feilds from the model Persons from the module sign_In.
        

