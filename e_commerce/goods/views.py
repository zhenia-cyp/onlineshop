from django.core.paginator import Paginator
from django.shortcuts import render,  get_list_or_404
from goods.utils import q_search
from goods.models import Product


def catalog(request,category_slug=None):

    page = request.GET.get('page',1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    search = request.GET.get('q', None)

    if category_slug  == "all-products":
        goods = Product.objects.all()

    elif search:
        goods = q_search(search)

    else:
        goods = get_list_or_404(Product.objects.filter(category__slug=category_slug))

    
    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    
    context = {'goods': current_page,
               'slug_url': category_slug}
    return render(request, 'goods/catalog.html', context)


def product(request, slug=None):

    if slug:
        product = Product.objects.get(slug=slug)
        return render(request, 'goods/product.html', {'product': product})
