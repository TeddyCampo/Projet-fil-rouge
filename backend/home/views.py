# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import User

def index(request):
    return HttpResponse("A lil' test")

def top_five(request):
    top_players_list = User.objects.order_by('-top_score')[:5]
    latest_players_list = User.objects.order_by('-date_joined')[:5]
    return render(request, 'home/home.html', {
        'top_players_list': top_players_list,
        'latest_players_list': latest_players_list})

# class IndexView(generic.ListView):
#     template_name='sondages/index.html'
#     context_object_name='latest_question_list'

#     def get_queryset(self):
#         return Question.objects.order_by('-pub_date')[:5]

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'sondages/detail.html'

# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'sondages/results.html'

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'sondages/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#     return HttpResponseRedirect(reverse('sondages:results', args=(question_id,)))

# def newQ(request):
    
#     question.question_text = request.POST['question']
    
#     return HttpResponseRedirect('sondages:')