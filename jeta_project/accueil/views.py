from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from .models import CustomUser, Field, Theme, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, PlayerProgressSerializer
from .forms import CustomUserCreationForm, ParagraphErrorList
from rest_framework import serializers

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
        user = request.user
        score = request.POST["score"]
        user.top_score = score
        user.save()
        message = "Score received: " + score
    return HttpResponse(message)

def get_score(request):
    if request.method == "GET":
        print("I received a get")
        username = request.user.username
        user = CustomUser.objects.get(username=username)
        score = user.top_score
    return JsonResponse({"score": score})

def get_q_and_a(request):
    if request.method == "GET":
        field = Field.objects.get(pk=1)
        theme = Theme.objects.filter(field=field.pk).first()
        questions = []
        answers = []
        some_questions = Question.objects.filter(theme=theme.pk)
        for q in some_questions:
            serializer = QuestionSerializer(q)
            questions.append(serializer.data)
            some_answers = Answer.objects.filter(question=q.pk)
            for a in some_answers:
                answerserializer = AnswerSerializer(a)
                answers.append(answerserializer.data)
    return JsonResponse({"questions": questions, "answers": answers})