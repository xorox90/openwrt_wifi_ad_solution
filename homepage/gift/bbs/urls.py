from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('bbs',
    (r'^$', 'views.list'),
    (r'^view/(?P<entity_id>\d+)/', 'views.view'),
    (r'^write/$', 'views.write'),
    (r'^modify/(?P<entity_id>\d+)/', 'views.modify'),
   
    #(r'^(?P<dutch_slug>[\w\d]+$)', 'views.dutch_table'),

)
