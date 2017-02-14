from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect

#importing models
#from .models import

def event(request):
    return HttpResponse("connected to xpense-server")

def installed(request):
	context = {
	}
	return render(request, 'flockapp/installed.html', context)

# def getsessionvar(request):
# 	userid = ''
# 	name = ''
# 	picture = ''
# 	email = ''
# 	if request.session.has_key('userid'):
# 			userid = request.session['userid']
# 			name = request.session['name']
# 			picture = request.session['picture']
# 			email = request.session['email']
# 	context = {
# 		'suserid' : userid,
# 		'sname' : name,
# 		'spicture' : picture,
# 		'semail' : email,
# 	}
# 	return context
