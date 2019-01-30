# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def top_five(request):
    top_players_list = User.objects.order_by('-top_score')[:5]
    latest_players_list = User.objects.order_by('-date_joined')[:5]
    return render(request, 'home/index.html', {
        'top_players_list': top_players_list,
        'latest_players_list': latest_players_list})
