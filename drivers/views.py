from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone

from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

from drivers.models import *
from drivers.forms import *


class NextRace:
    next_race = ''

    def get_next_race():
        now = datetime.now(timezone.utc)

        list = Schedule.objects.all()
        lowest_delta = 99999999
        for gp in list:
            delta = (gp.race - now).total_seconds()
            if delta < 0:
                continue
            elif delta < lowest_delta:
                next_race = gp
                lowest_delta = delta
        return next_race


class Home(NextRace, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Strona główna'
        queryset = Driver.objects.all().order_by('-points')
        context["object_list"] = queryset
        query = Schedule.objects.all()
        context["gp_list"] = query
        teams = Team.objects.all()
        context["team_list"] = teams
        context["next_race"] = NextRace.get_next_race()
        return context


class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Rejestracja'
        return context

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(self.request, user)
            messages.success(request, f'Pomyślnie stworzono konto {username}!')
            return redirect('home')
        else:
            form = RegisterForm()
            messages.warning(request, f'Wprowadź poprawne dane')
            return redirect('register')


class Login(auth_views.LoginView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Logowanie'
        return context


class Logout(auth_views.LogoutView):
    template_name = 'logout.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Wylogowanie'
        return context


@method_decorator(login_required, name='dispatch')
class Profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Mój profil'
        context["user_update"] = UserUpdateForm
        return context


class Map(TemplateView):
    template_name = 'race.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Nowa strona'
        return context

    def post(self, request):
        context = self.get_context_data(self)
        gp = request.POST.get('Gp', None)
        for race in Schedule.objects.all():
            if gp == race.full_name:
                gp = race
                break
            else:
                continue
        context["gp"] = gp

        return render(request, 'race.html', context)


@method_decorator(login_required, name='dispatch')
class Types(NextRace, FormView):
    template_name = 'types.html'
    form_class = TypeForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Typowanie'
        context["next_race"] = NextRace.get_next_race()
        return context

    def post(self, request):
        form = TypeForm(request.POST)
        if form.is_valid():
            usr = request.user
            ranking = ''
            rankingList = Ranking.objects.all()
            for rank in rankingList:
                if rank.username == usr:
                    ranking = rank
                    break
                else:
                    continue
            if ranking is '':
                ranking = Ranking(username=usr)
                ranking.save()
            form.save(commit=False)
            first = form.cleaned_data.get('first')
            second = form.cleaned_data.get('second')
            third = form.cleaned_data.get('third')
            race = NextRace.get_next_race()

            prediction = Prediction(user=usr,
                                    race=race, ranking=ranking, first=first, second=second, third=third)
            prediction.save()
            return redirect('types')
        else:
            form = TypeForm()
            messages.warning(request, f'Wprowadź poprawne dane')
            return redirect('types')
