from goods.models import Product
from carts.models import Cart
from django.shortcuts import redirect
from django.template.loader import render_to_string
from carts.utils import get_user_carts
from django.http import JsonResponse



def cart_add(request):
    product_id = request.POST.get("product_id")
    product = Product.objects.get(id=int(product_id))
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity +=1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)

    data = {
        "message": "Item add to cart",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(data)

def cart_change(request, product_id):
    pass

def cart_remove(request):
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()
    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request)
    data = {
        "message": "Item removed",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(data)
