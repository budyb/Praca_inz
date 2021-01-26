from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Count
from drivers.models import Driver, Prediction, Season, Result, HistoricResult


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=40, required=True, help_text='Obowiązkowe', label="Login")
    first_name = forms.CharField(
        max_length=40, required=False, help_text='Opcjonalne', label="Imię")
    last_name = forms.CharField(
        max_length=40, required=False, help_text='Opcjonalne', label="Nazwisko")
    email = forms.EmailField(max_length=254, help_text='Obowiązkowe')
    password1 = forms.CharField(widget=forms.PasswordInput(
    ), label="Hasło", help_text="Hasło musi się składać przynajmniej z 8 znaków")
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label="Wprowadź ponownie hasło")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=40, required=False, help_text='Obowiązkowe', label="Login")
    email = forms.EmailField(max_length=254, required=False, help_text='Obowiązkowe')
    password = forms.CharField(widget=forms.PasswordInput(
    ), label="Hasło", required=False, help_text="Hasło musi się składać przynajmniej z 8 znaków")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=40, required=True, label="Login")
    password = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Hasło")

    class Meta:
        model = User
        fields = ['username', 'password']


class TypeForm(forms.ModelForm):
    drivers = Driver.objects.all()
    first = forms.ModelChoiceField(
        queryset=drivers.order_by("surname"), label="1st")
    second = forms.ModelChoiceField(
        queryset=drivers.order_by("surname"), label="2nd")
    third = forms.ModelChoiceField(
        queryset=drivers.order_by("surname"), label="3rd")

    class Meta:
        model = Prediction
        fields = ['first', 'second', 'third']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# class ResultsForm(forms.ModelForm):
#     year = forms.ModelChoiceField(queryset=Season.objects.all().order_by('year'))
#     results= HistoricResult.objects.values_list('gpName').order_by('season__year').distinct()#.filter(season__year=2017)
#     # results = results.values_list('gpName')
#     # print(type(results))
#     # print(results[1])
#     # # res=[]
#     # for re in results:
#     #     re = str(re).replace("'","dsasdadas")
#     #     print(re)

#     # # print(results[1]['gpName'])
#     # print(results)
#     #print(results['gpName'])
#     #results = results.group_by["gp.full_name"]
#     result = forms.ModelChoiceField(queryset=results, to_field_name='gpName' )

#     class Meta:
#         model = Season
#         fields = ['year']