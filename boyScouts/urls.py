"""IDBSAV1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path , include
from . import views 
app_name = 'boyScouts'




urlpatterns = [
    path('login',views.loginView,name='loginView'),
    path('logout',views.logoutView,name='logoutView'),
    path('profile',views.profile,name='profile'),
    path('scoutList/<int:id>',views.scoutsList,name='scoutList'),
    path('scoutDetails/<int:id>',views.scoutDetails,name='scoutDetails'),
    path('scoutBadges/<int:id>',views.editScoutBadges,name='editScoutBadges'),
    path('admission',views.admission,name='admissionForm'),
    path('formset',views.formset),
]
