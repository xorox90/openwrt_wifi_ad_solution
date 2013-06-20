from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from product.models import ProductPlugin as ProductPluginModel
from django.utils.translation import ugettext as _

class ProductPlugin(CMSPluginBase):
	model = ProductPluginModel
	name = _("Product")
	render_template = "product.html"
	
	def render(self,context, instance, placeholder):
		products = instance.products.filter(category=instance.category)
		context.update({'products':products, 'category':instance.category})
		return context

plugin_pool.register_plugin(ProductPlugin)

