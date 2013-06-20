# -*- coding: utf-8 -*-
from django.db import models
class Entity(models.Model):
	title = models.TextField()
	password = models.TextField()
	content = models.TextField()
	onlyadmin = models.BooleanField()

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ["-id"]
		verbose_name_plural = "게시물"

class Reply(models.Model):
	entity = models.ForeignKey(Entity)
	admin = models.BooleanField()
