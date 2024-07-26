from goods.utils import q_search
from goods.models import Product
from django.http import Http404
from django.views.generic import DetailView, ListView
from django.core.cache import cache
from django.conf import settings



class CatalogView(ListView):
    model = Product
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 3

    def get_queryset(self,  **kwargs):
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")
        cache_key = settings.CACHE_NAME
        products_cache_name = cache.get(cache_key)
        if category_slug == "all-products":
            if products_cache_name:
                goods = products_cache_name
            else:
                goods = super().get_queryset()
                cache.set(cache_key, goods, timeout=60*5)
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()
        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Catalog"
        context["slug_url"] = self.kwargs.get('category_slug')
        return context


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
