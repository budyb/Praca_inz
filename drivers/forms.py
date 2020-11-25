from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=40, required=True, help_text='Obowiązkowe', label="Login")
    first_name = forms.CharField(max_length=40, required=False, help_text='Opcjonalne', label="Imię")
    last_name = forms.CharField(max_length=40, required=False, help_text='Opcjonalne', label="Nazwisko")
    email = forms.EmailField(max_length=254, help_text='Obowiązkowe')
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Hasło", help_text="Hasło musi się składać przynajmniej z 8 znaków")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Wprowadź ponownie hasło")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=40, required=True, help_text='Obowiązkowe', label="Login")
    email = forms.EmailField(max_length=254, help_text='Obowiązkowe')

    class Meta:
        model = User
        fields = ['username', 'email']

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=40, required=True, label="Login")
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Hasło")

    class Meta:
        model = User
        fields = ['username','password']