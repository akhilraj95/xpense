from django.conf.urls import url

from . import views

urlpatterns = [
	#Flock Event Listener URL
    url(r'^events$', views.events, name='events'),
    url(r'^installed$', views.installed, name='installed'),
]
