from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
  url(r'^admin/', include(admin.site.urls)),
	url(r'^munki/', include('munkimanager.urls')),
  url(r'^syncthing/', include('syncthingmanager.urls')),
  url(r'^django-rq/', include('django_rq.urls')),
)
