from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^manifests/([0-9a-zA-Z]+)/$', views.manifest),
	url(r'^info/([0-9a-zA-Z]+)/$', views.computerInfo),
	url(r'^autoenroll/$', views.autoEnroll),
	url(r'^datarequest/([0-9a-zA-Z]+)/$', views.enrollmentRequest, name="munki-data-request"),
	url(r'^selectinstall/([0-9a-zA-Z]+)/$', views.selectInstall, name="munki-select-install"),
)