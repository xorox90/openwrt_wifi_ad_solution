from django.contrib import admin
from product.models import *
from cms.admin.placeholderadmin import PlaceholderAdmin

admin.site.register(Category)
#admin.site.register(Seller)
admin.site.register(Product)
