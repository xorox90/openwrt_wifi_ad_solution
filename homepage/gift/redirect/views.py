# Create your views here.
from django.shortcuts import get_object_or_404, render

def index(request):
	redirect = request.GET.get('redirect')
	if(redirect == None):
		redirect = "http://naver.com"
	return render(request, 'index.html', {'redirect' : redirect })
