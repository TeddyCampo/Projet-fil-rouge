from django.shortcuts import render
from datetime import datetime
from .models import Player

# Create your views here.

def accueil(request):
    return render(request, 'accueil/index.html')

def top_five(request):
    top_players_list = Player.objects.order_by('-top_score')[:5]
    latest_players_list = Player.objects.order_by('-date_joined')[:5]
    return render(request, 'accueil/index.html', {
        'top_players_list': top_players_list,
        'latest_players_list': latest_players_list })

def project(request):
    return render(request, 'accueil/project.html')

def profs(request):
    return render(request, 'accueil/profs.html')

def faq(request):
    return render(request, 'accueil/faq.html')

def game(request):
    return render(request, 'accueil/game.html')

def sign(request):
    return render(request, 'accueil/sign.html')
