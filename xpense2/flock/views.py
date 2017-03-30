from django.shortcuts import render
from django.http import HttpResponse,Http404

# Create your views here.


def events(request):
    raise Http404("testing")


def config(request):
    context = {
    }
    return render(request, 'flock/config.html', context)
