from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil),
    path('project', views.project),
    path('profs', views.profs),
    path('faq', views.faq),
    path('game', views.game)
]