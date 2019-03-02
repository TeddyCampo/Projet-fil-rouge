from django.urls import path
from django.conf.urls import include, url
from . import views

urlpatterns = [
    path('', views.top_five, name='top_five'),
    path('project', views.project),
    path('profs', views.profs),
    path('faq', views.faq),
    path('game', views.game),
    path('signup', views.signup),
    url(r'^update_score/', views.update_score),
    url(r'^get_score/', views.get_score),
    url(r'^get_q_and_a/', views.get_q_and_a)
]
