from goods.models import Product
from carts.models import Cart
from django.template.loader import render_to_string
from carts.utils import get_user_carts
from django.http import JsonResponse
from django.urls import reverse
from django.views import View

class CartAddView(View):
    def post(self, request):
            product_id = request.POST.get("product_id")
            product = Product.objects.get(id=int(product_id))
            if request.user.is_authenticated:
                carts = Cart.objects.filter(user=request.user, product=product)
                if carts.exists():
                    cart = carts.first()
                    if cart:
                        cart.quantity += 1
                        cart.save()
                else:
                    Cart.objects.create(user=request.user, product=product, quantity=1)
            else:
                carts = Cart.objects.filter(
                    session_key=request.session.session_key, product=product)
                if carts.exists():
                    cart = carts.first()
                    if cart:
                        cart.quantity += 1
                        cart.save()
                else:
                    Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

            user_cart = get_user_carts(request)
            cart_items_html = render_to_string(
                "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

            data = {
                "message": "Item add to cart",
                "cart_items_html": cart_items_html,
            }
            return JsonResponse(data)


class CartChangeView(View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        quantity = request.POST.get("quantity")
        cart = Cart.objects.get(id=cart_id)
        cart.quantity = quantity
        cart.save()
        updated_quantity = cart.quantity
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}
        referer = request.META.get('HTTP_REFERER')
        if reverse('orders:create_order') in referer:
            context["order"] = True
        cart_items_html = render_to_string(
            "carts/includes/included_cart.html", context, request=request)
        data = {
            "message": "Quantity changed",
            "cart_items_html": cart_items_html,
            "quantity": updated_quantity,
        }
        return JsonResponse(data)


class CartRemoveView(View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")
        cart = Cart.objects.get(id=cart_id)
        quantity = cart.quantity
        cart.delete()
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}
        referer = request.META.get('HTTP_REFERER')
        if reverse('orders:create_order') in referer:
            context["order"] = True
        cart_items_html = render_to_string(
            "carts/includes/included_cart.html", context, request=request)
        data = {
            "message": "Item removed",
            "cart_items_html": cart_items_html,
            "quantity_deleted": quantity,
        }
        return JsonResponse(data)
