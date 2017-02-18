from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import flockapplib.jwtauth as jwt
import flockapplib.actions as action
import flockapplib.exports as export
import json
from django.http import HttpResponseRedirect

#importing models
from .models import Currency,User,Track,Expense,Chat,ChatExpense,Chattrack



@csrf_exempt
def events(request):
    if(jwt.verify(request.META['HTTP_X_FLOCK_EVENT_TOKEN'])):
        pjson = json.loads(request.body)
        if(pjson['name']=='app.install'):
            if(action.appinstall(pjson)):
                return HttpResponse("OK")
            else:
                raise Http404("testing")
        # elif(pjson['name']=='chat.receiveMessage'):
        #     if(action.receiveMessage(pjson)):
        #         return HttpResponse("OK")
        elif(pjson['name']=='client.messageAction'):
            print(pjson)
            user = User.objects.get(userId=str(pjson['userId']))
            message_uni = pjson['messageUids']
            message = []
            message.append(str(message_uni[0]))
            print(str(pjson['chat']))
            print(user)
            print(message)
            action.fetchMessage(str(pjson['chat']),user,message)
            return HttpResponse("""{"text": "Saved the bill"}""")
        else:
            print(request.body)
    raise Http404("testing")
    #return HttpResponse("connected to xpense-server")

def installed(request):
    context = {
    }
    return render(request, 'flockapp/installed.html', context)

def widget(request):
    if(jwt.verify(request.GET['flockEventToken'])):
        currency_list = Currency.objects.all()
        context = {
            'currency_list' : currency_list,
        }

        #Getting group information
        flockEvent = request.GET['flockEvent']
        pjson = json.loads(flockEvent)
        cmd_text = pjson['text']
        chat_id = str(pjson['chat'])
        chat_name = pjson['chatName']
        username = pjson['userName']
        userId = pjson['userId']
        cmd_text = pjson['text']

        cmd_text=cmd_text.lower()
        if(cmd_text=="list"):
            ################################################################### DONE
            user = User.objects.get(userId = userId)
            current_chat = Chat.objects.filter(chatId = chat_id)
            current_track = Chattrack.objects.filter(user = current_chat,active=True)
            if(len(current_track)==0):
                return HttpResponse("You aren't tracking yet. Try /Xpense to start tracking.")
            else:
                message = 'The list of '+current_track[0].name+' expenses are,\n'
                ch_list = ChatExpense.objects.filter(track=current_track)
                for expense in ch_list:
                    message = message+str(expense.currency.abbr)+' '+str(expense.amount)+' by '+str(expense.paidbywhom)+' for '+str(expense.purpose)+'\n'
                context['chatexpense_list'] = ch_list
                context['current_track'] = current_track[0]
                context['message'] = message
                context['userId'] = str(userId)
                context['chatId'] = str(chat_id)
                return render(request, 'flockapp/listexpense.html', context)
        elif(cmd_text=='close'):
            ################################################################# done
            user = User.objects.get(userId = userId)
            current_chat = Chat.objects.filter(chatId = chat_id)
            current_track = Chattrack.objects.filter(user = current_chat,active=True)
            if(len(current_track)==0):
                return HttpResponse("You aren't tracking yet. Try /Xpense to start tracking.")
            else:
                current_track[0].active = False
                current_track[0].save()
                action.sendGroupMessage(str(chat_id),user,'Xpense tracking of '+current_track[0].name+' closed.')
                context['userId'] = str(userId)
                context['track'] = current_track[0]
                context['chatId'] = str(chat_id)
                return render(request, 'flockapp/closetrack.html', context)
        elif(cmd_text=='report'):
            ################################################################# Done
            context['userId'] = str(userId)
            context['chatId'] = str(chat_id)
            chat = Chat.objects.get(chatId = str(chat_id))
            track_list = Chattrack.objects.filter(user=chat)
            context['track_list'] = track_list
            return render(request, 'flockapp/report.html', context)
        elif(cmd_text=='delete'):
            context['userId'] = str(userId)
            context['chatId'] = str(chat_id)
            chat = Chat.objects.get(chatId = str(chat_id))
            track_list = Chattrack.objects.filter(user=chat)
            context['track_list'] = track_list
            return render(request, 'flockapp/deletetrack.html', context)
        else:
            current_chat = Chat.objects.filter(chatId = chat_id)
            if(len(current_chat)==0):
                Chat(name=str(chat_name),chatId=str(chat_id)).save()

            current_track = Chattrack.objects.filter(user = current_chat,active=True)
            if(len(current_track)==0):
                context['id'] = chat_id
                context['userId'] = str(userId)
                return render(request, 'flockapp/starttrack.html', context)
            else:
                user = User.objects.get(userId = userId)
                context['chatId'] = current_track[0].user.chatId
                context['userId'] = str(userId)
                if(str(chat_id)[0]=='g'):
                    #group
                    group_members = action.getMembers(chat_id,user)
                    context['group_members'] = group_members
                else:
                    context['username'] = username
                return render(request, 'flockapp/widget.html', context)
    else:
        raise Http404("wth you doing bro?")

def closewidget(request):
    context = {}
    return render(request, 'flockapp/close.html', context)

@csrf_exempt
def starttrack(request):
    chatId = request.POST['chatId']
    userId = request.POST['userId']
    trackname = request.POST['trackname']
    purpose = request.POST['purpose']
    current_chat = Chat.objects.get(chatId=str(chatId))
    Chattrack(name=str(trackname),user=current_chat,purpose=purpose).save()
    user = User.objects.get(userId=str(userId))
    action.sendGroupMessage(chatId,user,'I have added Xpense tracker '+str(trackname)+' for '+str(purpose))
    return HttpResponse('ok')

@csrf_exempt
def deletetrack(request):
    chatId = request.POST['chatId']
    userId = request.POST['userId']
    trackId = request.POST['trackId']
    chat = Chat.objects.get(chatId=str(chatId))
    chattrack = Chattrack.objects.get(id=trackId,user=chat)
    track_name = chattrack.name
    chattrack.delete()
    user = User.objects.get(userId=str(userId))
    action.sendGroupMessage(chatId,user,'Track '+track_name+' deleted.')
    return HttpResponse('ok')

@csrf_exempt
def generatereport(request):
    chatId = request.POST['chatId']
    userId = request.POST['userId']
    trackId = request.POST['trackId']
    link_to_report = export.generate_report_2(trackId,chatId,userId)
    user = User.objects.get(userId=str(userId))
    current_chat = Chat.objects.get(chatId=str(chatId))
    current_track = Chattrack.objects.get(user = current_chat,id= str(trackId))
    #action.sendGroupMessage(chatId,user,'<flockml><a href="'+link_to_report+'">'+current_track.name+' pdf</a></flockml>')
    action.sendAttachment(chatId,user,link_to_report,current_track.name)
    return HttpResponse('ok')

@csrf_exempt
def sendmessage(request):
    chatId = request.POST['chatId']
    userId = request.POST['userId']
    message = request.POST['message']
    user = User.objects.get(userId=str(userId))
    action.sendGroupMessage(chatId,user,message)
    return HttpResponse('ok')

@csrf_exempt
def addexpense(request):
    chatId = request.POST['chatId']
    currency = request.POST['currency']
    amount = request.POST['amount']
    paidby = request.POST['paidby']
    purpose = request.POST['purpose']
    userId = request.POST['userId']
    current_chat = Chat.objects.get(chatId=str(chatId))
    current_track = Chattrack.objects.get(user = current_chat,active=True)
    currency = Currency.objects.get(id=str(currency))
    ChatExpense(track=current_track,amount=str(amount),currency=currency,paidbywhom=str(paidby),purpose=str(purpose),equallyshared=True).save()
    user = User.objects.get(userId=str(userId))
    action.sendGroupMessage(chatId,user,"Xpense Tracker: "+str(currency.abbr)+" "+str(amount)+" "+" paid by "+str(paidby)+" for "+str(purpose))
    return HttpResponse('ok')
