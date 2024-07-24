import json

import pytest
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.http import JsonResponse
from goods.models import Product
from carts.models import Cart
from .views import CartAddView, CartChangeView, CartRemoveView
from goods.models import Category
from django.core.files.base import ContentFile
from users.models import User
from django.urls import reverse


@pytest.fixture
def product():
    category = Category.objects.create(name="Test Category", slug="test-category")
    product = Product.objects.create(
        category=category,
        name="Test Product",
        slug="test-product",
        description="Test Description",
        price=10.00,
    )
    product.image.save("test_image.jpg", ContentFile(b"image content"), save=False)
    product.save()
    return product

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='12345',
        email='testuser@example.com'
    )

@pytest.fixture
def cart(user, product):
    return Cart.objects.create(user=user, product=product, quantity=1)

@pytest.fixture
def request_factory():
    return RequestFactory()

def add_session_to_request(request):
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()

@pytest.mark.django_db
class TestCartAddView:

    def test_add_to_cart_authenticated(self, request_factory, user, product):
        request = request_factory.post('/', data={'product_id': product.id})
        request.user = user
        add_session_to_request(request)

        view = CartAddView.as_view()
        response = view(request)

        assert isinstance(response, JsonResponse)
        assert response.status_code == 200
        assert Cart.objects.filter(user=user, product=product).exists()

    def test_add_to_cart_unauthenticated(self, request_factory, product):
        request = request_factory.post('/', data={'product_id': product.id})
        request.user = AnonymousUser()
        add_session_to_request(request)

        view = CartAddView.as_view()
        response = view(request)

        assert isinstance(response, JsonResponse)
        assert response.status_code == 200
        assert Cart.objects.filter(session_key=request.session.session_key, product=product).exists()


@pytest.mark.django_db
class TestCartChangeView:

    def test_cart_change_view(self, request_factory, user, cart):
        url = reverse('carts:cart_change')
        data = {
            'cart_id': cart.id,
            'quantity': 3
        }
        request = request_factory.post(url, data=data)
        request.user = user
        request.META['HTTP_REFERER'] = reverse('orders:create_order')
        view = CartChangeView.as_view()
        response = view(request)
        assert response.status_code == 200
        json_response = json.loads(response.content.decode('utf-8'))
        assert json_response['message'] == "Quantity changed"
        assert 'cart_items_html' in json_response
        assert json_response['quantity'] == '3'
        cart.refresh_from_db()
        assert cart.quantity == 3


    def test_cart_change_view_invalid_cart_id(self, request_factory, user):
        url = reverse('carts:cart_change')
        data = {
            'cart_id': 9999,
            'quantity': 3
        }
        request = request_factory.post(url, data=data)
        request.user = user

        view = CartChangeView.as_view()
        with pytest.raises(Cart.DoesNotExist):
            view(request)


@pytest.mark.django_db
class TestCartRemoveView:

    def test_cart_remove_view(self, user, cart, request_factory):
        url = reverse('carts:cart_remove')
        data = {'cart_id': cart.id}
        request = request_factory.post(url, data)
        request.user = user
        request.META['HTTP_REFERER'] = 'http://testserver/'

        view = CartRemoveView.as_view()
        response = view(request)

        assert response.status_code == 200
        assert Cart.objects.filter(id=cart.id).count() == 0

        response_data = response.content.decode('utf-8')
        response_json = json.loads(response_data)

        assert response_json['message'] == 'Item removed'
        assert response_json['quantity_deleted'] == 1


    def test_cart_remove_view_nonexistent_cart(self, user, request_factory):
        url = reverse('carts:cart_remove')
        data = {'cart_id': 7377}
        request = request_factory.post(url, data)
        request.user = user
        request.META['HTTP_REFERER'] = 'http://testserver/'

        view = CartRemoveView.as_view()
        with pytest.raises(Cart.DoesNotExist):
            view(request)
