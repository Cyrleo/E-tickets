from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms





class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username" , "email" , "password1" , "password2"]

        widgets={
            "username" : forms.TextInput(),
            "email" : forms.EmailInput(),
            "password1" : forms.PasswordInput()
        }
        help_texts = {
            "username": None

        }

    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()