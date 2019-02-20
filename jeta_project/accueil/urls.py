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
    path('signup', views.signup),
    url(r'^update_counter/', views.update_counter)
]
