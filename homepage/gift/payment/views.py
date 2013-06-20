# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django import forms
from payment.models import *
import datetime
from datetime import timedelta
from django.utils.timezone import utc
import random, string
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.db import transaction
from django.core.urlresolvers import reverse

class BuyForm(forms.Form):
	recipient = forms.CharField()
	
class DutchForm(forms.Form):
	recipient = forms.CharField(label="선물 받으실 분 핸드폰 번호") 
	#msg = forms.CharField(label="남기실 메세지")
	slug = forms.SlugField(label="공유 링크")
	sponsor = forms.IntegerField(label="더치페이 인원수",initial=2)

def buy(request,product_id):
	product = get_object_or_404(Product,id=product_id)
	
	return render(request, 'product_detail.html', {'product' : product })

def dutch_table(request, dutch_slug):
	dutch = get_object_or_404(Dutch, slug=dutch_slug)
	payment = dutch.payment
	product = payment.product
	dutch_table = DutchTable.objects.all().filter(dutch=dutch)
	recipient = SMSRecipient.objects.get(payment=payment)
	destination = recipient.HPP_Num
	return render(request, 'dutch_table.html', {'destination':destination, 'product':product, 'payment':payment, 'dutch':dutch, 'dutch_table' :dutch_table })


@transaction.commit_on_success
def dutch(request,product_id):
	form=None

	product = get_object_or_404(Product,id=product_id)
	if(request.method == 'POST'):
		form = DutchForm(request.POST)
		if(form.is_valid()):	
			try:
				sponsor = form.cleaned_data['sponsor']
				price = product.price
				mod = price % sponsor
				price -= mod
				
				prices = [price/sponsor+mod]

				for x in range(sponsor-1):
					prices.append(price/sponsor)			

				payment = Payment()
				payment.recipient = form.cleaned_data['recipient']
				payment.product = product
				#payment.msg = form.cleaned_data['msg']
				payment.save()


				recipient=SMSRecipient()
				recipient.payment = payment
				recipient.HPP_Num = form.cleaned_data['recipient']
				recipient.save()
				
				dutch = Dutch()
				dutch.payment = payment
				dutch.slug = form.cleaned_data['slug']
				now = datetime.datetime.utcnow().replace(tzinfo=utc)
				dutch.close_date = now + timedelta(days=7)
				dutch.save()

				First=True
				dutchId=None
				for x in prices:
					dutchTable = DutchTable()
					dutchTable.dutch = dutch
					dutchTable.money = x
					dutchTable.payed = False
					dutchTable.save()
					if(First):
						dutchId=dutchTable.id
						First=False
				print(reverse('payment.views.dutch_table', args=(dutch.slug,)))
				return HttpResponseRedirect(reverse('payment.views.dutch_table', args=(dutch.slug,)))
				#return HttpResponseRedirect("http://jmm.kr/pg/dutch.php?id="+str(dutchId))
			except:
				return HttpResponseBadRequest(content="알 수 없는 예외가 일어났습니다. 관리자에게 문의하십시요")

	slug = ''
	while(True):
		slug = ''.join(random.sample(string.ascii_lowercase+string.digits,5))
		try:
			now = datetime.datetime.utcnow().replace(tzinfo=utc)	
			Dutch.objects.get(slug=slug, close_date_gt=now)
		except:
			break
	
	if(form is None):
		form = DutchForm(initial={'slug':slug, 'product':product_id})				
	return render(request, 'dutch.html', {'product' : product, 'form' : form})

	
