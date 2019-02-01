from django.shortcuts import render
from django.http import HttpResponse

def game_view(request):
    return render(request, 'game/index.html', content_type="text/html")

# def game_view(request):
#     return HttpResponse("A test", content_type="text/html")