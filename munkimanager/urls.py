from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
  url(r'^manifests/([0-9a-zA-Z\- _]+)$', views.manifest, name="munki-manifest"),
	url(r'^info/([0-9a-zA-Z]+)/$', views.computerInfo, name='munki-computer-info'),
	url(r'^autoenroll/$', views.autoEnroll),
	url(r'^datarequest/([0-9a-zA-Z]+)/$', views.enrollmentRequest, name="munki-data-request"),
	url(r'^selectinstall/([0-9a-zA-Z]+)/$', views.selectInstall, name="munki-select-install"),
)