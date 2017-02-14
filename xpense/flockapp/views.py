from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import flockapplib.jwtauth as jwt
import flockapplib.actions as action
import json

#importing models
#from .models import



@csrf_exempt
def events(request):
    if(jwt.verify(request.META['HTTP_X_FLOCK_EVENT_TOKEN'])):
        pjson = json.loads(request.body)
        if(pjson['name']=='app.install'):
            if(action.appinstall(pjson)):
                return HttpResponse("OK")
            else:
                raise Http404("testing")
        else:
            print(request.body)
    raise Http404("testing")
    #return HttpResponse("connected to xpense-server")

def installed(request):
    context = {
    }
    return render(request, 'flockapp/installed.html', context)
