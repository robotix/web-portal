from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import logout

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'fms.views.index', name='index'),
    url(r'^admin/', include('grappelli.urls')),
    url(r'^masteradmin/', include(admin.site.urls)),
    url(r'^team/', include('team.urls', namespace='team')),
    url(r'^participant/', include('participant.urls', namespace='participant')),
    url(r'^add/(?P<model_name>\w+)/?$', 'tekextensions.views.add_new_model'),
)