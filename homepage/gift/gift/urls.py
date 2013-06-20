# -*- coding: utf-8 -*-

from django.conf.urls import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
#from django.views.generic.simple import redirect_to

admin.autodiscover()

from cms.models import Page 
Page._meta.verbose_name_plural = "페이지"

from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.contrib import admin

admin.site.unregister(Site)
admin.site.unregister(User)
admin.site.unregister(Group)

#urlpatterns = i18n_patterns('',
urlpatterns = patterns('',
    # Examples:
    # url(r'^gift/', include('gift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^$', 'gift.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
    #(r'^dutch/(?P<dutch_slug>[\w\d]+)$','payment.views.dutch_table'),
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
