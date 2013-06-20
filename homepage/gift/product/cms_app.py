from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
class ProductApp(CMSApp):
	name = _("Product App")
	urls = ["product.urls"]

apphook_pool.register(ProductApp)
