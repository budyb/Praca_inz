from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, date
from .forms import ContactForm
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django_group_by import GroupByMixin

from drivers.models import *
from drivers.forms import *


class NextRace: 
    def get_next_race():
        now = datetime.now(timezone.utc)
        next_race = ''
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
        query = Schedule.objects.all().order_by('race')
        context["gp_list"] = query
        context["next_race"] = NextRace.get_next_race()
        return context

        
class Classification(NextRace, TemplateView):
    template_name = 'classification.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Klasyfikacja kierowców'
        queryset = Driver.objects.all().order_by('-points')
        context["object_list"] = queryset
        return context

class TeamClassification(NextRace, TemplateView):
    template_name = 'team_classification.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Klasyfikacja konstruktorów'
        teams = Team.objects.all().order_by('-points')
        context["team_list"] = teams
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
    form_class = UserUpdateForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Mój profil'
        context["user_update"] = self.form_class
        return context

    def post(self, request):
        form = UserUpdateForm(request.POST,instance=request.user)
        user = self.request.user 
        if request.method == 'POST':
            if form.is_valid():
                raw_password = form.cleaned_data.get('password')
                form.save()
                user.set_password(raw_password)
                user.save()                
                messages.success(request,'Zaktualizowano profil!')
                return redirect('home')
            else:
                form = UserUpdateForm(instance=request.user)
                context = self.get_context_data(self)
                return render(request, 'profile.html',context )

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
        results = Result.objects.filter(season__year=2020).filter(gp=gp)
        context["gp"] = gp
        context["results"] = results
        context["title"] = gp.full_name

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
            race = NextRace.get_next_race()
            today = date.today()
            if race.race.date() == today:
                form = TypeForm()
                messages.warning(request, f'Typowanie w dzień wyścigu jest zablokowane')
                return redirect('types')
            for rank in rankingList:
                if rank.username == usr:
                    ranking = rank
                    for prediction in ranking.Predictions.all():
                        if prediction.race.full_name == race.full_name:
                            messages.warning(
                                request, f'Wytypowałeś już wyniki tego wyścigu')
                            return redirect('types')
                        else:
                            continue
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

            prediction = Prediction(
                                    race=race, ranking=ranking, first=first, second=second, third=third)

            prediction.save()
            messages.success(request, f'Wytypowano wyniki!')
            return redirect('home')
        else:
            form = TypeForm()
            messages.warning(request, f'Wprowadź poprawne dane')
            return redirect('types')

class Results(TemplateView):
    template_name = 'results.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["seasons"] = Season.objects.all().order_by('year')
        context["title"] = 'Nowa strona'
        return context

    def post(self, request):
        context = self.get_context_data(self)
        season_id = request.POST['Rok']
        if season_id:
            race_name = request.POST['Race']
            season = Season.objects.get(id=season_id) 
            if not race_name:        
                context['show'] = "show"       
                if season.year < 2020:
                    context['season'] = season
                    context['historic_races'] = HistoricResult.objects.filter(season=season).group_by('gpName').distinct()
                else:
                    context['season'] = season
                    context['races'] = Result.objects.filter(season=season).group_by('season','gp__full_name').distinct()
                
                
                return render(request, 'results.html', context)
            else:
                
                if season.year < 2020:
                    context['historic_results'] = HistoricResult.objects.filter(season=season, gpName=race_name)
                else:
                    context['results'] = Result.objects.filter(season=season, gp__full_name= race_name)

                return render(request, 'results.html', context)
        else:
            messages.warning(request, f'Wybierz sezon!')
            return render(request, 'results.html', context)

@method_decorator(login_required, name='dispatch')
class RankingView(TemplateView):
    template_name = 'ranking.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Ranking'
        context["rankings"] = Ranking.objects.all().order_by('-points')
        return context

class Contact(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['settings'] = settings
        context['form'] = ContactForm
        context["title"] = 'Kontakt'
        return context

    def post(self, request, **kwargs):
        if request.method == 'POST':

            context = self.get_context_data(self)
            form = ContactForm(request.POST)
            if form.is_valid():
                sender_name = form.cleaned_data['name']
                sender_email = form.cleaned_data['email']

                message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['message'])
                send_mail('New Enquiry', message, sender_email, ['MarcinCzuba3@gmail.com'])
                messages.success(request,"Dziala")
                return redirect('home')
        else:
            form = ContactForm()

        return render(request, 'contact.html', context)


class DriverView(TemplateView):
    template_name = 'driver.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Nowa strona'
        return context

    def post(self, request):
        context = self.get_context_data(self)
        drver = request.POST.get('driver', None)
        
        for driver in Driver.objects.all():
            if drver == str(driver):
                drver = driver
                break
            else:
                continue
        context["driver"] = drver
        context["title"] = drver
        return render(request, 'driver.html', context)

class TeamView(TemplateView):
    template_name = 'team.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Nowa strona'
        return context

    def post(self, request):
        context = self.get_context_data(self)
        given_team = request.POST.get('team', None)
        
        for team in Team.objects.all():
            if given_team == str(team):
                given_team = team
                break
            else:
                continue
        context["team"] = given_team
        context["title"] = given_team
        return render(request, 'team.html', context)

@method_decorator(login_required, name='dispatch')
class TypesHistory(TemplateView):
    template_name = 'types_history.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["settings"] = settings
        context["title"] = 'Historia typów'
        return context

    def get(self, request):        
        user = request.user
        context = self.get_context_data(self)
        if request.method == 'GET':
            predictions = Prediction.objects.filter(ranking__username=user)
            context["prediction_list"]=predictions
            return render(request, 'types_history.html', context)