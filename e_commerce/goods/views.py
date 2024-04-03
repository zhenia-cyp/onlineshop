from django.core.paginator import Paginator
from django.shortcuts import render,  get_list_or_404

from goods.models import Product


def catalog(request,category_slug=None):

    page = request.GET.get('page',1)


    if category_slug  == "all-products":
        goods = Product.objects.all()

    else:
        goods = get_list_or_404(Product.objects.filter(category__slug=category_slug))

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    
    context = {'goods': current_page,
               'slug_url': category_slug}
    return render(request, 'goods/catalog.html', context)


def product(request, slug=None):

    if slug:
        product = Product.objects.get(slug=slug)
        return render(request, 'goods/product.html', {'product': product})
