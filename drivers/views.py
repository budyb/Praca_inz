from django.shortcuts import render, redirect
import logging
from drivers.models import Driver
from django.contrib.auth import login, authenticate

from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.conf import settings
import requests

from drivers.forms import RegisterForm


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        queryset = Driver.objects.all()
        context["object_list"] = queryset

        return context

class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        return context

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password=raw_password)
            login(self.request, user)
            return redirect('home')
    