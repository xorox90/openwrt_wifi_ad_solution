from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class BBSApp(CMSApp):
	name = _("BBS App")
	urls = ["bbs.urls"]

apphook_pool.register(BBSApp)
