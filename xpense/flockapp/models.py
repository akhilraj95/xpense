from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30, blank = True, default = 'user')
    userId = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    def __str__(self):
        return self.userId

class Chat(models.Model):
    name = models.CharField(max_length=30, blank = True, default = 'user')
    chatId = models.CharField(max_length=100)
    def __str__(self):
        return self.chatId

class Chattrack(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('Chat', default = None , blank = True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    purpose = models.CharField(max_length=200,default='none')
    def __str__(self):
        return self.name

class ChatExpense(models.Model):
    track = models.ForeignKey('Chattrack', default = None , blank = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default = 0.0)
    currency = models.ForeignKey('Currency', default = None , blank = True)
    #paidby = models.ForeignKey('User', default = None , blank = True)
    paidbywhom = models.CharField(max_length=30,default='none')
    purpose = models.CharField(max_length=100, default = 'Unspecified')
    equallyshared = models.BooleanField(default=False)
    def __str__(self):
        return self.track.name+' '+self.purpose+' '+str(self.amount)

class Bills(models.Model):
    image = models.ImageField()
    track = models.ForeignKey('Chattrack', default = None , blank = True)

class Currency(models.Model):
    name = models.CharField(max_length=20)
    abbr = models.CharField(max_length=5)
    def __str__(self):
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey('User', default = None , blank = True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Expense(models.Model):
    track = models.ForeignKey('Track', default = None , blank = True)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default = 0.0)
    currency = models.ForeignKey('Currency', default = None , blank = True)
    paidby = models.ForeignKey('User', default = None , blank = True)
    purpose = models.CharField(max_length=100, default = 'Unspecified')
    equallyshared = models.BooleanField(default=False)
    def __str__(self):
        return self.track.name+' '+self.purpose+' '+str(self.amount)
