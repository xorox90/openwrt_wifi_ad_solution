from django.conf.urls import *

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('product',
    (r'^(?P<product_id>\d+)/', 'views.detail' ),
)
