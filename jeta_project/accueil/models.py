from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import datetime


class Field(models.Model):
    fieldName = models.CharField(max_length=200)

    def __str__(self):
        return self.fieldName


class Theme(models.Model):
    themeName = models.CharField(max_length=200)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return self.themeName


class Level(models.Model):
    levelName = models.CharField(max_length=200)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    maxScore = models.IntegerField()
    indexNumber = models.IntegerField()

    def __str__(self):
        return self.levelName


class Question(models.Model):
    questionText = models.CharField(max_length=200)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.questionText


class Answer(models.Model):
    answerText = models.CharField(max_length=200)
    isCorrect = models.BooleanField(default=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answerText

class Teacher(models.Model):
    #A voir si necessaire de rajouter d'autres attributs plus tard
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class Player(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    top_score = models.IntegerField('high score', default=0)
    # date_joined = models.DateTimeField('date joined')
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def was_published_recently(self):
        return self.date_joined >= timezone.now() - datetime.timedelta(days=1)


class PlayerProgress(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return self.player.username, self.score
