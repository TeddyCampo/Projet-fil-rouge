from django.shortcuts import render
from datetime import datetime
from .models import Player
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

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

@login_required
def game(request):
    return render(request, 'accueil/game.html')

# def login(request):
#     return render(request, 'registration/login.html')

# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         return render(request, 'accueil/index.html')
#     else:
#         return render(request, "<p> Merci d'entrer un identifiant valide ou de vous inscrire </p>")
