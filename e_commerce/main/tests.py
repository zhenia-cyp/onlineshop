import pytest
from django.urls import reverse
from django.test import RequestFactory
from .views import IndexView, AboutView

@pytest.mark.django_db
class TestIndexView:
    def test_index_view_template(self):
        path = reverse('main:index')
        request = RequestFactory().get(path)
        response = IndexView.as_view()(request)
        assert response.template_name == ['main/index.html']

    def test_index_view_context(self):
        path = reverse('main:index')
        request = RequestFactory().get(path)
        response = IndexView.as_view()(request)
        assert 'content' in response.context_data
        assert response.context_data['content'] == "Harmony Home Furnishings"

@pytest.mark.django_db
class TestAboutView:
    def test_about_view_template(self):
        path = reverse('main:about')
        request = RequestFactory().get(path)
        response = AboutView.as_view()(request)
        assert response.template_name == ['main/about.html']

    def test_about_view_context(self):
        path = reverse('main:about')
        request = RequestFactory().get(path)
        response = AboutView.as_view()(request)
        assert response.context_data is not None
        assert 'content' not in response.context_data