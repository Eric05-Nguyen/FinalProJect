from django.shortcuts import render
from django.core.paginator import Paginator
from product.models import Product
from django.shortcuts import get_object_or_404

def index(request):
    products = Product.objects.all().order_by('-id')[:6]
    return render(request, 'index.html', {'products': products})

def shop(request):
    product_list = Product.objects.all().order_by('-id')
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'shop.html', {'products': products})

