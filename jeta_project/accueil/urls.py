from django.urls import path
from django.conf.urls import include, url
from . import views
from django.views.generic.base import TemplateView  # new

urlpatterns = [
    # path('', views.accueil),
    path('', views.top_five, name='top_five'),
    path('project', views.project),
    path('profs', views.profs),
    path('faq', views.faq),
    path('game', views.game),
    path('signup', views.signup)
    # path('accounts/', include('django.contrib.auth.urls')),  #Chemin de test pour la config du login
    # path('', TemplateView.as_view(template_name='game.html'), name='game'),  # new
]
