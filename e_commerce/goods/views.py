from django.http import HttpResponse
from django.shortcuts import render,  get_list_or_404

from goods.models import Product


def catalog(request,category_slug=None):


    if category_slug  == "all-products":
        goods = Product.objects.all()

    else:
        goods = get_list_or_404(Product.objects.filter(category__slug=category_slug))

    
    return render(request, 'goods/catalog.html',{'goods': goods})


def product(request, slug=None):

    if slug:
        product = Product.objects.get(slug=slug)


    return render(request, 'goods/product.html', {'product': product})
