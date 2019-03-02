from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

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


class Question(models.Model):
    questionText = models.CharField(max_length=200)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    index = models.IntegerField()

    class Meta:
        unique_together = ("theme", "index")

    def __str__(self):
        return self.questionText


class Answer(models.Model):
    answerText = models.CharField(max_length=200)
    isCorrect = models.BooleanField(default=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answerText


class CustomUser(AbstractUser):
    top_score = models.IntegerField('high score', default=0)
    themes = models.ManyToManyField(Theme)

    def __str__(self):
        return self.username

    def was_published_recently(self):
        return self.date_joined >= timezone.now() - datetime.timedelta(days=1)
