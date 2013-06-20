from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class PaymentApp(CMSApp):
	name = _("Payment App")
	urls = ["payment.urls"]

apphook_pool.register(PaymentApp)
