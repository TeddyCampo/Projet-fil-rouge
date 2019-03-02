from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from .models import CustomUser, Field, Theme, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, ThemeSerializer
from .forms import CustomUserCreationForm, ParagraphErrorList
from rest_framework import serializers
import random


def accueil(request):
    return render(request, 'accueil/index.html')


def top_five(request):
    top_players_list = CustomUser.objects.order_by('-top_score')[:5]
    latest_players_list = CustomUser.objects.order_by('-date_joined')[:5]
    return render(request, 'accueil/index.html', {
        'top_players_list': top_players_list,
        'latest_players_list': latest_players_list})


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
        form = CustomUserCreationForm(
            request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            try:
                with transaction.atomic():
                    user = CustomUser.objects.filter(username=username)

                    if not user.exists():
                        user = CustomUser.objects.create(username=username)
                        user.set_password(password)
                        user.save()
                        # login user
                        login(request, user)
                        return redirect('/game')
                    else:
                        user = user.first()

            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."
    else:
        form = CustomUserCreationForm()
    context['form'] = form
    context['errors'] = form.errors.items()
    return render(request, 'accueil/signup.html', context)


def update_score(request):
    message = ''
    if request.method == "POST":
        """ Get the current player and save his new score """
        user = request.user
        score = request.POST["score"]
        user.top_score = score
        user.save()
        message = "Score received: " + score
        """ Just a message to check if score correctly saved """
    return HttpResponse(message)


def get_score(request):
    if request.method == "GET":
        print("I received a score request !")
        """ Get the name of the current player """
        username = request.user.username
        user = CustomUser.objects.get(username=username)
        """ Get his score from the database """
        score = user.top_score
    return JsonResponse({"score": score})


def get_q_and_a(request):
    if request.method == "GET":
        print("I received a q_and_a request !")
        """ Get the field from the DB (equal to 1 because there is only Geography) """
        field = Field.objects.get(pk=1)
        """ Get the theme related to the field ("first()" because only one theme) """
        username = request.user.username
        # user = CustomUser.objects.get(username=username)

        userThemes = Theme.objects.filter(
            customuser__username__contains=username)
        allThemes = Theme.objects.all()
        if userThemes.count() == allThemes.count():
            # random theme chosen
            randomPK = random.randint(1, allThemes.count())
            print(randomPK)
            # Output single theme in order to do question and answer searches
            themeToUse = allThemes.get(pk=randomPK)
            print(themeToUse.themeName)
        else:
            for themeDone in userThemes:
                allThemes = allThemes.exclude(pk=themeDone.pk)
            themeToUse = allThemes.first()
            print(themeToUse.themeName)

        theme = ThemeSerializer(themeToUse).data

        questions = []
        answers = []
        """ Get the questions related to the theme """
        some_questions = Question.objects.filter(theme=themeToUse.pk)
        """ Serialize the questions into a json object and push them in an array """
        for q in some_questions:
            serialized_question = QuestionSerializer(q).data
            questions.append(serialized_question)
            """ Get the answers related to the questions """
            some_answers = Answer.objects.filter(question=q.pk)
            """ Serialize the answers and push in array """
            for a in some_answers:
                serialized_answer = AnswerSerializer(a).data
                answers.append(serialized_answer)
    """ Return a json object with both questions and answers arrays """
    return JsonResponse({"questions": questions, "answers": answers, "theme": theme})


def get_next_theme(request):
    # From url query, capture the theme pk of the last used theme
    themeSent = request.GET.get('theme', '')
    # Get the theme from the database
    theme = Theme.objects.get(pk=themeSent)
    # Add the theme to the CustomUser's profile
    user = CustomUser.objects.get(username=request.user.username)
    user.themes.add(theme)
    # Send data to game for the next level
    get_q_and_a(request)
    return HttpResponse("Another theme has been chosen!")
