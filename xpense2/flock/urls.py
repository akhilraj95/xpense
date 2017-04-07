from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    #flock events url
    url(r'^events$', views.events, name='events'),
    #flock configuration url
    url(r'^config$', views.config, name='config'),
    #flock chattab
    url(r'^chattab$', views.chattab, name='chattab'),
    #flock chattabaction
    url(r'^chattabaction$', views.chattabaction, name='chattabaction'),
    #flock slash
    url(r'^slash$', views.slash, name='slash'),
    #flock start track
    url(r'^start$', views.start, name='start'),
    #flock add expense
    url(r'^add$', views.add, name='add'),
    #flock viewing track
    url(r'^track$', views.track, name='track'),
    #flock deleting track
    url(r'^delete$', views.delete, name='delete'),
    #flock adding bill through Message action bank
    url(r'^mab$', views.mab, name='mab'),
    #flock handling bill addition
    url(r'^bill$', views.bill, name='bill'),
    #flock handling report request
    url(r'^report$', views.report, name='report'),
    #flock handling report request
    url(r'^sendreport$', views.sendreport, name='sendreport'),
    #flock delete report
    url(r'^deleteexpense$', views.deleteexpense, name='deleteexpense'),

]
