from django.urls import path
from .views import catalog, ProductView

app_name ='goods'

urlpatterns = [
    path('search/', catalog, name='search'),
    path('<slug:category_slug>/', catalog, name='index'),
    path('product/<slug:slug>/', ProductView.as_view(), name='product'),
]