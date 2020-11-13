from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=40, required=True, help_text='Obowiazkowe' )
    first_name = forms.CharField(max_length=40, required=False, help_text='Obowiazkowe.')
    last_name = forms.CharField(max_length=40, required=False, help_text='Obowiazkowe')
    email = forms.EmailField(max_length=254, help_text='Obowiazkowe')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']