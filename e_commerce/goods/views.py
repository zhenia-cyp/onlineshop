from django.core.paginator import Paginator
from django.shortcuts import render,  get_list_or_404
from goods.utils import q_search
from goods.models import Product
from django.http import Http404
from django.views.generic import DetailView


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    search = request.GET.get('q', None)

    if category_slug == "all-products":
        goods = Product.objects.all()

    elif search:
        goods = q_search(search)

    else:
        goods = Product.objects.filter(category__slug=category_slug)
        if not goods.exists():
            raise Http404()

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))
    
    context = {'goods': current_page,
               'slug_url': category_slug}
    return render(request, 'goods/catalog.html', context)


class ProductView(DetailView):
    template_name = "goods/product.html"
    context_object_name = "product"

    def get_object(self, *args, **kwargs):
        product_slug = self.kwargs.get('slug')
        if product_slug:
            try:
                return Product.objects.get(slug=product_slug)
            except Product.DoesNotExist:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context
