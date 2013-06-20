#-*- coding: utf-8 -*-

from django.db import models
from cms.models import CMSPlugin
from sorl.thumbnail import ImageField
class Category(models.Model):
	name = models.TextField()

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "카테고리"

#class Seller(models.Model):
#	name = models.TextField()
#	
#	def __unicode__(self):
#		return self.name

class Product(models.Model):
	name = models.TextField()
	description = models.TextField()
	price = models.IntegerField()
	category = models.ForeignKey(Category)
	#seller = models.ForeignKey(Seller)

	def path(self,filename):
		return '/'.join([self.category.name, filename])

	image = ImageField(upload_to=path)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = "제품"

class ProductPlugin(CMSPlugin):
	category = models.ForeignKey(Category)
	products = Product.objects.all()
	def __unicode__(self):
		return self.category.name	

	def copy_relations(self,oldinstance):
		self.category = oldinstance.category


# Create your models here.
