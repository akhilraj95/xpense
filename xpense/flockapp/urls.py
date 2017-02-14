from django.conf.urls import url

from . import views

urlpatterns = [
	#Flock Event Listener URL
    url(r'^event$', views.event, name='event'),
    url(r'^installed$', views.installed, name='installed'),
]
