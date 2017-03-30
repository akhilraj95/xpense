from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import secret,action
import json


#FlockOS
from pyflock import FlockClient, verify_event_token
from pyflock import Message, SendAs, Attachment, Views, WidgetView, HtmlView, ImageView, Image, Download, Button, OpenWidgetAction, OpenBrowserAction, SendToAppAction

from models import User

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
    except:
        raise Http404("(-__-) 404!")

# Configuration URL
def config(request):
    context = {
    }
    return render(request, 'flock/config.html', context)

@xframe_options_exempt
def slash(request):
    context = {}
    event_token = request.GET['flockEventToken']
    app_secret = secret.getAppSecret()
    verify_event_token(event_token = event_token, app_secret = app_secret)

    #Getting group information
    flockEvent = request.GET['flockEvent']
    pjson = json.loads(flockEvent)
    chat_id = str(pjson['chat'])
    chat_name = pjson['chatName']
    username = pjson['userName']
    userId = pjson['userId']
    cmd_text = pjson['text']

    #Getting user token
    context['userId'] = userId
    context['chat_id'] = chat_id
    context['chat_name'] = chat_name
    context['username'] = username

    if cmd_text == '' or cmd_text =='help':
        return render(request, 'flock/slash_help.html', context)
    elif cmd_text == 'start':
        return render(request, 'flock/start.html', context)
    elif cmd_text == 'close':
        return render(request, 'flock/slash_help.html', context)
    elif cmd_text == 'add':
        return render(request, 'flock/slash_help.html', context)
    elif cmd_text == 'delete':
        return render(request, 'flock/slash_help.html', context)
    elif cmd_text == 'list':
        return render(request, 'flock/slash_help.html', context)
    elif cmd_text == 'status':
        return render(request, 'flock/slash_help.html', context)
    elif cmd_text == 'print':
        return render(request, 'flock/slash_help.html', context)


def start(request):
    print request.POST['chat_id']
    return HttpResponse("OK")
