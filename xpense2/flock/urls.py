from django.conf.urls import url

from . import views

urlpatterns = [
    #flock events url
    url(r'^events$', views.events, name='events'),
    #flock configuration url
    url(r'^config$', views.config, name='config'),
    #flock slash
    url(r'^slash$', views.slash, name='slash'),
    #flock start track
    url(r'^start$', views.start, name='start'),

]
