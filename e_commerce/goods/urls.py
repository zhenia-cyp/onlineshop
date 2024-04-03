from django.urls import path
from .views import catalog, product

app_name ='goods'

urlpatterns = [
    path('<slug:category_slug>/', catalog, name='index'),
    path('<slug:category_slug>/<int:page>/', catalog, name='index'),
    path('product/<slug:slug>/', product, name='product'),

]