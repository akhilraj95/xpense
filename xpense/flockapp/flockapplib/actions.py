# Flock actions library for event handling
# author : Akhil Raj Azhikodan
# date   : 14th feb,2017
#
#  FLock Functions:
#     appinstall(parsed_json)
#     appuninstall(parsed_json)
#     receiveMessage(parsed_json)
#
#  Bot Functions:
#     bot_sendMessage(userId,message)
#     bot_receiveMessage(text,from_userId,timestamp)
#
#  Bot Helper:
#     Bot feature classes map (refer in bot helper section)
#
#
#  Note : Flockappsecret is gitignored. The file contains the confidential app secret.
#        Contact author for the file

from .. import models
import requests
import flockappsecret as secret
import urllib,urllib2
from django.db.models import Q
import exports
import json

# Save userId and token in to db on install. sends a welcome message to the user.
def appinstall(pjson):
    try:
        userId = pjson['userId']
        token = pjson['token']
        u = models.User(userId = userId, token=token)
        u.save()
        bot_sendMessage(userId,"Hey there, I am XpenseBot. I can assit you in drafting your expense report for your travel, managing group budget and managing group expenses.Go ahead do your job, I will worry about the expenses")
        return True
    except:
        return False

# Removes the user from the db
def appuninstall(pjson):
    userId = pjson['userId']
    models.User.objects.get(userId = userId).delete()
    return

# Handles the receives message from userId
def receiveMessage(pjson):
    try:
        message = pjson['message']
        text = message['text']
        from_userId = message['from']
        to_userId = message['to']
        timestamp = message['timestamp']

        #If the message is addressed for the bot
        if(to_userId == secret.getBotUserId()):
            bot_receiveMessage(text,from_userId,timestamp)
        return True
    except:
        return False

def getMembers(group_id,user):
    data = [('groupId',str(group_id)),('token',str(user.token))]
    url = 'https://api.flock.co/v1/groups.getMembers'
    req = urllib2.Request(url, headers={'Content-Type' : 'application/x-www-form-urlencoded'})
    print('GETTING MEMBERS('+group_id+'):')
    result = urllib2.urlopen(req, urllib.urlencode(data))
    content = result.read()
    return json.loads(content)

def sendGroupMessage(chatId,user,text):
    data = [('to',str(chatId)),('token',str(user.token)),('text',str(text))]
    url = 'https://api.flock.co/v1/chat.sendMessage'
    req = urllib2.Request(url, headers={'Content-Type' : 'application/x-www-form-urlencoded'})
    print('SENDINGMESSAGE('+chatId+'):')
    result = urllib2.urlopen(req, urllib.urlencode(data))
    content = result.read()
    return

def sendAttachment(chatId,user,text,name):
    fil = [{"downloads": [{ "src": str(text) },]}]
    data = [('to',str(chatId)),('token',str(user.token)),('text',name+'_report'),('attachments',fil)]
    url = 'https://api.flock.co/v1/chat.sendMessage'
    req = urllib2.Request(url, headers={'Content-Type' : 'application/x-www-form-urlencoded'})
    print('SENDINGMESSAGE('+chatId+'):')
    print(data)
    print(urllib.urlencode(data))
    result = urllib2.urlopen(req, urllib.urlencode(data))
    content = result.read()
    return
    return


###############################################################################################
## BOT ACTIONS
###############################################################################################

# Method to send message to any user
def bot_sendMessage(userId,message):
    data = [('to',userId),('text',message),('token',secret.getBotToken())]
    url = 'https://api.flock.co/v1/chat.sendMessage'
    req = urllib2.Request(url, headers={'Content-Type' : 'application/x-www-form-urlencoded'})
    print(data)
    result = urllib2.urlopen(req, urllib.urlencode(data))
    content = result.read()
    print(content)
    return

def bot_receiveMessage(text,from_userId,timestamp):
    text = text.lower()
    text = text.split()
    command = text[0]+' '+text[1]
    feature = feature_class_map(command)
    if(feature==-1.0):
        bot_sendMessage(from_userId,'Sorry, I didnt get that.')
    elif(feature==1.1):
        print("test")
        ##################- start tracking -#########################
        #checking if already tracking
        usr = models.User.objects.get(userId = from_userId)
        if(models.Track.objects.filter(user = usr, active = True).count()!=0):
            bot_sendMessage(from_userId,'You are already tracking. Close the last track with, complete tracking')
        else:
            if(len(text)>=3):
                nm = text[2]
                nm = nm.lower()
                trk = models.Track(name=nm,user = usr)
                trk.save()
                bot_sendMessage(from_userId,'Sure, I will start tracking '+text[2]+' expenses right away.')
            else:
                bot_sendMessage(from_userId,'Try, start tracking <track-name>')
    elif(feature==1.2):
        bot_sendMessage(from_userId,'Adding user')
    elif(feature==1.3):
        #################- Adding Expense -##########################
        if(len(text)>=7):
            cmd1 = text[2]
            cmd2 = text[5]
            if(cmd1.lower() == 'paid' and cmd2.lower() == 'for'):
                currency = text[3]
                amt = float(text[4])
                purpose = text[6]
                for i in range(7,len(text)):
                    purpose = purpose+' '+ text[i]
                usr = models.User.objects.get(userId = from_userId)
                cur_obj = models.Currency.objects.filter(Q(name__icontains=currency)| Q(abbr__icontains=currency))
                if(len(cur_obj)>0):
                    trk_obj = models.Track.objects.get(active=True,user=usr)
                    models.Expense(track = trk_obj,amount = amt,currency=cur_obj[0],purpose=purpose,paidby=usr).save()
                    bot_sendMessage(from_userId,'Expense added, paid '+currency+' '+str(amt)+' for '+purpose)
                else:
                    bot_sendMessage(from_userId,'I dont understand the currency, try rupees,dollars,usd,inr..')
            else:
                bot_sendMessage(from_userId,'Try,add expense paid <currency(rupee/inr)> <amt> for <purpose>')
        else:
            bot_sendMessage(from_userId,'Try,add expense paid <currency(rupee/inr)> <amt> for <purpose>')
    elif(feature==1.5):
        #####################- Current Total Expense -###########################
        usr = models.User.objects.get(userId = from_userId)
        trk_obj = models.Track.objects.get(active=True,user=usr)
        cur_qs = models.Currency.objects.all()
        msg = 'The current total expense for '+trk_obj.name+' is'
        print(trk_obj)
        for cur in cur_qs:
            ex_qs = models.Expense.objects.filter(track = trk_obj,currency=cur)
            sum = 0.0
            for i in ex_qs:
                sum = sum + i.amount
            if(sum!=0):
                msg = msg +', '+ cur.name +' '+str(sum)
        bot_sendMessage(from_userId,msg)
        bot_sendMessage('List the expenses tracked with, list expenses.')
    elif(feature==1.6):
        ##################- Total Expense till now-###############################
        usr = models.User.objects.get(userId = from_userId)
        trk_obj = models.Track.objects.get(active=True,user=usr)
        ex_qs = models.Expense.objects.filter(track = trk_obj)
        print(usr)
        print(trk_obj)
        print(ex_qs)
        msg = ''
        for ex in ex_qs:
            tim = ex.timestamp.time()
            msg = msg +ex.currency.abbr+' '+str(ex.amount)+' for '+ex.purpose+' at '+str(tim.hour)+':'+str(tim.minute)+' on '+str(ex.timestamp.date())+'\n'
        bot_sendMessage(from_userId,msg)
    elif(feature==1.8):
        #################- terminate_tracking -########################
        usr = models.User.objects.get(userId = from_userId)
        trk = models.Track.objects.get(user = usr, active = True)
        trk.active = False
        trk.save()
        bot_sendMessage(from_userId,'Track '+trk.name+' closed.')
    elif(feature==2.0):
        ###################- Generate Report -#########################
        usr = models.User.objects.get(userId = from_userId)
        if(len(text)==3):
            nm = text[2]
            nm = nm.lower()
            trk = models.Track.objects.filter(Q(name__icontains=nm)| Q(user = usr))
            if(len(trk)>0):
                bot_sendMessage(from_userId,'Sure, generating report...')
                exports.generate_report(trk[0],usr)
        else:
            trk_qs = models.Track.objects.filter(user=usr)
            msg = 'try, generate report <name>,\nThe track names are,\n'
            for trk in trk_qs:
                msg = msg+' '+trk.name+'\n'
            bot_sendMessage(from_userId,msg)
    return

###############################################################################################
# BOT HELPER
###############################################################################################
#  Bot feature classes map
#      class-1: gibberish
#      class 0: travel_expense  (not_supported)
#               sub_class_1: start_tracking#
#               sub_class_2: add users to travel
#               sub_class_3: add_expense#
#               sub_class_4: remove_expense
#               sub_class_5: find current total expense#
#               sub_class_6: dump_expense_list
#               sub_class_7: edit_expense
#               sub_class_8: terminate_tracking
#      class 1: generate_report
#      class 2: budgeted_expenditure (not_supported)
#      class 3: approximate_cost (not_supported)

## KEYWORDS
command_sub_class_1 = 'start tracking'
command_sub_class_2 = 'add fellow'
command_sub_class_3 = 'add expense'
command_sub_class_4 = 'remove expense'
command_sub_class_5 = 'current total'
command_sub_class_6 = 'list expenses'
command_sub_class_8 = 'complete tracking'

command_class_2 = 'generate report'

def feature_class_map(text):
    if(text==command_sub_class_1):
        return 1.1
    elif(text==command_sub_class_2):
        return 1.2
    elif(text==command_sub_class_3):
        return 1.3
    elif(text==command_sub_class_4):
        return 1.4
    elif(text==command_sub_class_5):
        return 1.5
    elif(text==command_sub_class_6):
        return 1.6
    elif(text==command_sub_class_8):
        return 1.8
    elif(text==command_class_2):
        return 2.0
    return -1.0
