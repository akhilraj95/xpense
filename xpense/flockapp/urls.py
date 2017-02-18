from django.conf.urls import url

from . import views

urlpatterns = [
	#Flock Event Listener URL
    url(r'^events$', views.events, name='events'),
    url(r'^installed$', views.installed, name='installed'),
    url(r'^widget$', views.widget, name='widget'),
    url(r'^starttrack$',views.starttrack, name='starttrack'),
    url(r'^addexpense$',views.addexpense, name='addexpense'),
    url(r'^sendmessage$',views.sendmessage, name='sendmessage'),
    url(r'^generatereport$',views.generatereport, name='generatereport'),
    url(r'^deletetrack$',views.deletetrack, name='deletetrack'),
]
