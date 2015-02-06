from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
  url(r'^stubdevice/([0-9a-zA-Z\- _]+)/configdata/$', views.stubDeviceData, name="syncthing-stubdata"),
)