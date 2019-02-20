from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db import transaction
from .models import CustomUser
from .forms import CustomUserCreationForm, ParagraphErrorList

def accueil(request):
    return render(request, 'accueil/index.html')

def top_five(request):
    top_players_list = CustomUser.objects.order_by('-top_score')[:5]
    latest_players_list = CustomUser.objects.order_by('-date_joined')[:5]
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

@transaction.atomic
def signup(request):
    context = {}
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            try:
                with transaction.atomic():
                    user = CustomUser.objects.filter(username=username)
                    
                    if not user.exists():
                        user = CustomUser.objects.create(username=username)
                        user.set_password(password)

                        # user = CustomUser.objects.create(
                        #     top_score = 0
                        # )
                        user.save()
                        # login user
                        login(request, user)
                        return redirect('/')
                    else:
                        user = user.first()

                    # user.save()
                    # return redirect('/')

            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
    else:
        form = CustomUserCreationForm()
    context['form'] = form
    context['errors'] = form.errors.items()
    return render(request, 'accueil/signup.html', context)