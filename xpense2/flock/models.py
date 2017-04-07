from __future__ import unicode_literals
from django.db import models


# Stores only the users who install the app
class User(models.Model):
    userId = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.userId


class Currency(models.Model):
    name = models.CharField(max_length=20)
    abbr = models.CharField(max_length=5)
    def __str__(self):
        return self.name

class Chat(models.Model):
    chat_id = models.CharField(max_length=100)
    chat_name = models.CharField(max_length=100)
    def __str__(self):
        return self.chat_name

class Track(models.Model):
    name = models.CharField(max_length=50)
    chat = models.ForeignKey('Chat', default = None , blank = True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=100, default = 'Unspecified')
    active = models.BooleanField(default=True)
    budget_currency = models.ForeignKey('Currency', default = None , blank = True)
    budget = models.IntegerField(default=0.0, blank = True)
    def __str__(self):
        return self.name

class Expense(models.Model):
    track = models.ForeignKey('Track', default = None , blank = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default = 0.0)
    currency = models.ForeignKey('Currency', default = None , blank = True)
    paidby = models.CharField(max_length=100, default = 'Unspecified')
    purpose = models.CharField(max_length=100, default = 'Unspecified')
    def __str__(self):
        return self.track.name+' '+self.purpose+' '+str(self.amount)

class Bill(models.Model):
    expense = models.ForeignKey('Expense', default = None , blank = True)
    url = models.CharField(max_length=100, default = '')
    def __str__(self):
        return self.url
