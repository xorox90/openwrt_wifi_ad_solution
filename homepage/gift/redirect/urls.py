from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('redirect',
    (r'^', 'views.redirect'),

)
