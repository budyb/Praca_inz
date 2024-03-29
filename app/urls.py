"""dist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from drivers.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', Profile.as_view(), name='profile'),
    path('race/', Map.as_view(), name='map'),
    path('types/', Types.as_view(), name='types'),
    path('results/', Results.as_view(), name='results'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('classification/', Classification.as_view(), name='classification'),
    path('contact/', Contact.as_view(), name='contact'),
    path('team_classification/', TeamClassification.as_view(), name='TeamClassification'),
    path('driver/', DriverView.as_view(), name='driver'),
    path('team/', TeamView.as_view(), name='team'),
    path('types_history/', TypesHistory.as_view(), name='types_history')
]
