from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=40, required=True, help_text='Obowiązkowe' )
    first_name = forms.CharField(max_length=40, required=False, help_text='Opcjonalne')
    last_name = forms.CharField(max_length=40, required=False, help_text='Opcjonalne')
    email = forms.EmailField(max_length=254, help_text='Obowiązkowe')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']