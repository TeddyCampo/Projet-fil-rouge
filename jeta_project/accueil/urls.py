from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    # path('', views.accueil),
    path('', views.top_five, name='top_five'),
    path('project', views.project),
    path('profs', views.profs),
    path('faq', views.faq),
    path('game', views.game),
    path('login', views.login),
    # path('sign', include('django.contrib.auth.urls')) #Chemin de test pour la config du login
]
