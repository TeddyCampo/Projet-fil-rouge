from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import datetime

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

