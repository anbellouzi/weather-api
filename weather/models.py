import datetime
from django import forms
from django.db import models
from django.utils import timezone

class Mood(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    def __str__(self):
        return self.name