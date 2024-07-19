import pytest
from django.urls import reverse
from django.test import Client
from goods.models import Product, Category
from django.core.files.base import ContentFile

@pytest.fixture
def category():
    return Category.objects.create(name="Test Category", slug="test-category")

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
def client():
    return Client()

@pytest.mark.django_db
def test_product_view_success(client, product):
    url = reverse('goods:product', kwargs={'slug': product.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert b'Test Product' in response.content

@pytest.mark.django_db
def test_product_view_not_found(client):
    url = reverse('goods:product', kwargs={'slug': 'non-existent-slug'})
    response = client.get(url)
    assert response.status_code == 404