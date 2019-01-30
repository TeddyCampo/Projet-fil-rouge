from django.shortcuts import render
from datetime import datetime

# Create your views here.

def accueil(request):
    return render(request, 'accueil/index.html')

def project(request):
    return render(request, 'accueil/project.html')

def profs(request):
    return render(request, 'accueil/profs.html')

def faq(request):
    return render(request, 'accueil/faq.html')

def game(request):
    return render(request, 'accueil/game.html')