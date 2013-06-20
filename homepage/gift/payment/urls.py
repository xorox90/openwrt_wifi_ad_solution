from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('payment',
    (r'^buy/(?P<product_id>\d+)$', 'views.buy'),
    (r'^dutch/(?P<product_id>\d+)$', 'views.dutch'),
    #(r'^(?P<dutch_slug>[\w\d]+$)', 'views.dutch_table'),

)
