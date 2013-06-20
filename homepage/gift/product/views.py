# Create your views here.
from product.models import Product
from django.shortcuts import get_object_or_404, render

def detail(request,product_id):
	product = get_object_or_404(Product,id=product_id)
	
	return render(request, 'product_detail.html', {'product' : product })
