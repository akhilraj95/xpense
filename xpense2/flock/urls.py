from django.conf.urls import url

from . import views

urlpatterns = [
    #flock events url
    url(r'^events$', views.events, name='events'),
    #flock configuration url
    url(r'^config$', views.config, name='config'),
]
