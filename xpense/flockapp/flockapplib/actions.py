from .. import models
import requests
import flockappsecret as secret
import urllib,urllib2

def appinstall(pjson):
    try:
        userId = pjson['userId']
        token = pjson['userId']
        u = models.User(userId = userId, token=token)
        u.save()
        bot_sendMessage(userId,"Hey there, I am XpenseBot. I can assit you in drafting your expense report for your travel, managing group budget and managing group expenses.Go ahead do your job, I will worry about the expenses")
        return True
    except:
        return False

def bot_sendMessage(userId,message):
    data = [('to',userId),('text',message),('token',secret.getBotToken())]
    url = 'https://api.flock.co/v1/chat.sendMessage'
    req = urllib2.Request(url, headers={'Content-Type' : 'application/x-www-form-urlencoded'})
    print(data)
    result = urllib2.urlopen(req, urllib.urlencode(data))
    content = result.read()
    print(content)
    return
