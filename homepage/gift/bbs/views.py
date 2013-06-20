# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django import forms
from bbs.models import *
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.db import transaction
from django.core.urlresolvers import reverse
from django.core.paginator import *
from django.views.decorators.cache import never_cache
class WriteForm(forms.Form):
	title = forms.CharField()
	onlyadmin=forms.BooleanField(required=False)
	password = forms.CharField(widget=forms.PasswordInput())
	content = forms.CharField(widget=forms.Textarea)

@never_cache
def list(request):
	entities = Entity.objects.all()
	return render(request, 'list.html', {"entities":entities})

@never_cache
def write(request):
	if(request.method == 'POST'):
		form = WriteForm(request.POST)
		if(form.is_valid()):	
			entity = Entity()
			entity.password = form.cleaned_data['password']
			entity.title = form.cleaned_data['title']
			entity.content = form.cleaned_data['content']
			entity.onlyadmin = form.cleaned_data['onlyadmin']
			entity.save()
			
			return HttpResponseRedirect(reverse('bbs.views.view', args=(entity.id,)))
		else:			
			return HttpResponseBadRequest(content="양식이 잘못되었습니다.")

	else:	
		form = WriteForm()				
		return render(request, 'write.html', {'form' : form})

@never_cache
def view(request,entity_id):
	entity = get_object_or_404(Entity,id=entity_id)
	auth=False
	if (entity.onlyadmin and request.user.is_superuser) or not entity.onlyadmin:
		auth=True

	return render(request, 'view.html', {'entity' : entity, 'auth' :auth })
	
@never_cache
def modify(request,entity_id):
	entity = get_object_or_404(Entity, id=entity_id)
	if(request.method == 'POST'):
		form = WriteForm(request.POST)
		if(form.is_valid()):
			if(entity.password == form.cleaned_data['password'] or request.user.is_superuser):
				if('update' in request.POST):
					entity.title = form.cleaned_data['title']
					entity.content = form.cleaned_data['content']
					entity.onlyadmin = form.cleaned_data['onlyadmin']
					entity.save()			
					return HttpResponseRedirect(reverse('bbs.views.list'))
				elif('delete' in request.POST):
					entity.delete()
					return HttpResponseRedirect(reverse('bbs.views.list'))
				else:
					return HttpResponseBadRequest(content="잘못된 요청입니다")
			else:
				return HttpResponseBadRequest(content="비밀번호가 틀립니다.")
		else:
			return HttpResponseBadRequest(content="?")
		
					
	else:	
		form = WriteForm(initial={'title':entity.title, 'content':entity.content, 'onlyadmin':entity.onlyadmin})
		return render(request, 'modify.html', {'entity':entity, 'form' : form})
