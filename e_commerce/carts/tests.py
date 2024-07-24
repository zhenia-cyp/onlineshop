import pytest
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser, User
from django.http import JsonResponse
from goods.models import Product
from carts.models import Cart
from .views import CartAddView
from goods.models import Category
from django.core.files.base import ContentFile
from users.models import User


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
