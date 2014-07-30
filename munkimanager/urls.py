from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^manifests/([0-9a-zA-Z]+)/$', views.manifest),
	url(r'^info/([0-9a-zA-Z]+)/$', views.computerInfo),
)