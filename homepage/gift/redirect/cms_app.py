from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class RedirectApp(CMSApp):
	name = _("Redirect App")
	urls = ["redirect.urls"]

apphook_pool.register(RedirectApp)
