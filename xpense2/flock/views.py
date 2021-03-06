from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from csp.decorators import csp_update
from datetime import timedelta
import secret,action
import json



#FlockOS
from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction

from models import User,Chat,Track,Currency,Expense,Bill

# Event Listsener URL
@csrf_exempt
def events(request):
    try:
        event_token = request.META['HTTP_X_FLOCK_EVENT_TOKEN']
        app_secret = secret.getAppSecret()
        verify_event_token(event_token = event_token, app_secret = app_secret)
        pjson = json.loads(request.body)
        if(pjson['name']=='app.install'):
            action.appInstall(pjson)
            return HttpResponse("OK")
        if(pjson['name']=='app.uninstall'):
            action.appUninstall(pjson)
            return HttpResponse("OK")
    except:
        raise Http404("(-__-) 404!")

# Configuration URL
def config(request):
    context = {
        'user_count':User.objects.all().count(),
    }
    return render(request, 'flock/config.html', context)

def slash(request):
    '''listens to xpense slash commands and renders the modal'''
    event_token = request.GET['flockEventToken']
    app_secret = secret.getAppSecret()
    verify_event_token(event_token = event_token, app_secret = app_secret)

    #Getting group information
    flockEvent = request.GET['flockEvent']
    pjson = json.loads(flockEvent)
    print pjson
    chat_id = str(pjson['chat'])
    chat_name = pjson['chatName']
    username = pjson['userName']
    userId = pjson['userId']
    cmd_text = pjson['text']

    # #Getting user token
    # context['userId'] = userId
    # context['chat_id'] = chat_id
    # context['chat_name'] = chat_name
    # context['username'] = username
    #
    # #get all the currency
    # currency_list = Currency.objects.all()
    # context['currency_list'] = currency_list

    if cmd_text == '' or cmd_text =='help':
        return main_interface(request,userId,chat_id,chat_name,username,0)
    elif cmd_text == 'start':
        return main_interface(request,userId,chat_id,chat_name,username,1)
    elif cmd_text == 'add':
        return main_interface(request,userId,chat_id,chat_name,username,2)
    elif cmd_text == 'status':
        return main_interface(request,userId,chat_id,chat_name,username,3)
    elif cmd_text == 'delete':
        return main_interface(request,userId,chat_id,chat_name,username,4)
    elif cmd_text == 'report':
        return main_interface(request,userId,chat_id,chat_name,username,5)
    else:
        context ={}
        return render(request, 'flock/slash_help.html', context)

@csp_update(FRAME_SRC='self')
@xframe_options_exempt
def main_interface(request,userId,chat_id,chat_name,username,option):
    # option 0 - help
    # option 1 - start
    # option 2 - add
    # option 3 - status
    # option 4 - delete
    # option 5 - report
    context = {}

    #Getting user token
    context['userId'] = userId
    context['chat_id'] = chat_id
    context['chat_name'] = chat_name
    context['username'] = username

    print "option = ",option

    #get all the currency
    currency_list = Currency.objects.all()
    context['currency_list'] = currency_list

    if option == 0:
        return render(request, 'flock/slash_help.html', context)
    elif option == 1:
        return render(request, 'flock/start.html', context)
    elif option == 2:
        #get all tracks of the chat
        chatObjList = Chat.objects.filter(chat_id=chat_id)
        if len(chatObjList)==0:
            return render(request, 'flock/start.html', context)
        else:
            trackObjList = Track.objects.filter(chat = chatObjList[0])
            context['track_list'] = trackObjList
        #get all the members of the chat
        if chat_id[0] == 'g':
            user = User.objects.get(userId=userId)
            flock_client = FlockClient(token=user.token, app_id=secret.getAppID)
            member_list = flock_client.get_group_members(chat_id)
            context['member_list'] = member_list
            print member_list
        else:
            member_list = []
            member = {
                'firstName' : username,
                'lastName' : '',
                'id': userId,}
            member_list.append(member)
            member = {
                'firstName' : chat_name,
                'lastName' : '',
                'id': chat_id,}
            member_list.append(member)
            context['member_list'] = member_list
            print member_list
        return render(request, 'flock/add.html', context)
    elif option == 3:
        chatObjList = Chat.objects.filter(chat_id=chat_id)
        if len(chatObjList)==0:
            return render(request, 'flock/start.html', context)
        else:
            trackObjList = Track.objects.filter(chat = chatObjList[0])
            context['track_list'] = trackObjList
        return render(request, 'flock/status.html', context)
    elif option == 4:
        chatObjList = Chat.objects.filter(chat_id=chat_id)
        if len(chatObjList)==0:
            return render(request, 'flock/start.html', context)
        else:
            trackObjList = Track.objects.filter(chat = chatObjList[0])
            context['track_list'] = trackObjList
        return render(request, 'flock/delete.html', context)
    elif option == 5:
        chatObjList = Chat.objects.filter(chat_id=chat_id)
        if len(chatObjList)==0:
            return render(request, 'flock/start.html', context)
        else:
            trackObjList = Track.objects.filter(chat = chatObjList[0])
            context['track_list'] = trackObjList
        return render(request, 'flock/report_track.html', context)
    else:
        return render(request, 'flock/slash_help.html', context)


def start(request):
    '''Registers the chat if not registered before and starts a track'''
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    trackname = request.POST['trackname']
    purpose = request.POST['purpose']
    currency = request.POST['currency']
    budget = request.POST['budget']
    #Check if trackname is empty
    if trackname == '':
        action.sendMessage(chat_id,userId,"Xpense couldn't start track. Try again with another name")

    chatObjList = Chat.objects.filter(chat_id=chat_id)
    chatObj = 0
    #Register the chat if not already registered.
    if len(chatObjList)==0:
        #Register the chat
        chatObj = Chat(chat_id = chat_id,chat_name = chat_name)
        chatObj.save()
    else:
        chatObj = chatObjList[0]
    #creating track
    if currency != '':
        currencyObj = Currency.objects.get(id=currency)
        Track(name=trackname,chat =chatObj,purpose=purpose,budget=budget,budget_currency=currencyObj).save()
    else:
        Track(name=trackname,chat =chatObj,purpose=purpose,budget=budget).save()
    action.sendMessage(chat_id,userId,"Started a new track "+trackname)
    return HttpResponse("OK")


def add(request):
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    amount = request.POST['amount']
    paidby = request.POST['paidby']
    currency = request.POST['currency']
    track = request.POST['track']
    purpose = request.POST['purpose']
    url_list = []
    if 'url_list' in request.POST:
        url_list = json.loads(request.POST['url_list'])

    chatObj = Chat.objects.get(chat_id=chat_id)
    trackObj = Track.objects.get(id=track)
    currencyObj = Currency.objects.get(id= currency)
    #verify that the track belongs to that chat
    if trackObj.chat == chatObj:
        expenseObj = Expense(track=trackObj,amount=amount,currency = currencyObj,paidby = paidby,purpose=purpose)
        expenseObj.save()
        for url in url_list:
            Bill(expense = expenseObj, url = str(url)).save()
    return HttpResponse("OK")

@xframe_options_exempt
def track(request):
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    track_id = request.POST['track']
    print chat_id
    print userId
    print chat_name
    print username

    trackObj = Track.objects.get(id = track_id)
    #check if chat_id is same
    if(chat_id!=trackObj.chat.chat_id):
        return HttpResponse('ok')
    context = {
        'track': trackObj
    }
    if trackObj.budget != 0:
        context['budget'] = trackObj.budget



    expense_list = Expense.objects.filter(track = trackObj)

    #handling TIMEZONE
    user = User.objects.get(userId=userId)
    flock_client = FlockClient(token=user.token, app_id=secret.getAppID)
    pjson = flock_client.get_user_info()
    utc = str(pjson['timezone'])
    hours = int(utc[1:3])
    minutes = int(utc[4:6])
    if(utc[0]=='+'):
        for expense in expense_list:
            expense.timestamp += timedelta(hours=hours,minutes=minutes)
    else:
        for expense in expense_list:
            expense.timestamp -= timedelta(hours=hours,minutes=minutes)

    total_expense_by_curr,converted_total,perc_spent = action.total(expense_list,trackObj)
    context['expense_list'] = expense_list
    context['total_expense'] = total_expense_by_curr
    context['converted_total'] = converted_total
    context['perc_spent'] = perc_spent
    return render(request, 'flock/track.html', context)

def delete(request):
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    track_id = request.POST['track_id']

    trackObj = Track.objects.get(id = track_id)
    name = trackObj.name
    #check if chat_id is same
    if(chat_id!=trackObj.chat.chat_id):
        return HttpResponse('ok')
    trackObj.delete()
    action.sendMessage(chat_id,userId,"Deleted track - "+name)
    return HttpResponse('ok')

######################################################################### - chattab


@xframe_options_exempt
def chattab(request):
    context = {}
    event_token = request.GET['flockEventToken']
    app_secret = secret.getAppSecret()
    verify_event_token(event_token = event_token, app_secret = app_secret)

    #Getting group information
    flockEvent = request.GET['flockEvent']
    pjson = json.loads(flockEvent)
    print pjson
    chat_id = str(pjson['chat'])
    chat_name = pjson['chatName']
    username = pjson['userName']
    userId = pjson['userId']

    context['userId'] = userId
    context['chat_id'] = chat_id
    context['chat_name'] = chat_name
    context['username'] = username
    return render(request, 'flock/options.html', context)

def chattabaction(request):
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    action_id = int(request.POST['action'])
    return main_interface(request,userId,chat_id,chat_name,username,action_id)


########################################################################### - Message action Button
@csp_update(FRAME_SRC='self')
@xframe_options_exempt
def mab(request):
    context = {}
    event_token = request.GET['flockEventToken']
    app_secret = secret.getAppSecret()
    verify_event_token(event_token = event_token, app_secret = app_secret)
    flockEvent = request.GET['flockEvent']
    pjson = json.loads(flockEvent)
    print pjson
    messageUids = pjson['messageUids']
    chat_id = str(pjson['chat'])
    chat_name = pjson['chatName']
    username = pjson['userName']
    userId = pjson['userId']

    context['userId'] = userId
    context['chat_id'] = chat_id
    context['chat_name'] = chat_name
    context['username'] = username

    #get the url of the bills
    user = User.objects.get(userId=userId)
    token = user.token
    messageUids = [str(m) for m in messageUids]
    url_list = action.fetchMessagePictures(chat_id,token,messageUids)
    print url_list
    if len(url_list)==0:
        return HttpResponse('Bills must be JPEG or PNG')

    context['url_list'] = json.dumps(url_list)
    #get set of tracks
    chatObjList = Chat.objects.filter(chat_id=chat_id)
    if len(chatObjList)==0:
        return render(request, 'flock/start.html', context)
    else:
        trackObjList = Track.objects.filter(chat = chatObjList[0])
        context['track_list'] = trackObjList

    #get all members of the chat
    if chat_id[0] == 'g':
        user = User.objects.get(userId=userId)
        flock_client = FlockClient(token=user.token, app_id=secret.getAppID)
        member_list = flock_client.get_group_members(chat_id)
        context['member_list'] = member_list
        print member_list
    else:
        member_list = []
        member = {
            'firstName' : username,
            'lastName' : '',
            'id': userId,}
        member_list.append(member)
        member = {
            'firstName' : chat_name,
            'lastName' : '',
            'id': chat_id,}
        member_list.append(member)
        context['member_list'] = member_list

    #get all the currency
    currency_list = Currency.objects.all()
    context['currency_list'] = currency_list


    return render(request, 'flock/addbill.html', context)


def bill(request):
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    track_id = request.POST['track']
    url_list = request.POST['url_list']
    print track_id
    print url_list
    return HttpResponse('ok')


@csp_update(FRAME_SRC='self')
@xframe_options_exempt
def report(request):
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    track_id = request.POST['track']

    trackObj = Track.objects.get(id = track_id)
    file_src = action.report(trackObj,userId)
    context = {
        'file_src' : file_src,
        'track_name': trackObj.name,
    }
    context['userId'] = userId
    context['chat_id'] = chat_id
    context['chat_name'] = chat_name
    context['username'] = username

    return render(request, 'flock/report.html', context)

def sendreport(request):
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    track_name = request.POST['track_name']
    filename = request.POST['filename']
    print userId

    user = User.objects.get(userId=userId)
    flock_client = FlockClient(token=user.token, app_id=secret.getAppID)

    d = Download(src="http://www.xpense.com/"+filename)
    views = Views()
    views.add_flockml("<flockml>Download the <i>"+track_name+" report</i></flockml>")
    # NOTE: downloads is always a list
    attachment = Attachment(title="Test files", downloads=[d], views=views)
    files_message = Message(to=chat_id, attachments = [attachment])
    res = flock_client.send_chat(files_message)
    print(res)
    return HttpResponse('OK')

def deleteexpense(request):
    chat_id = request.POST['chat_id']
    userId = request.POST['userId']
    chat_name = request.POST['chat_name']
    username = request.POST['username']
    expense = request.POST['expense']
    Expense.objects.get(id = expense).delete()
    return HttpResponse('OK')
