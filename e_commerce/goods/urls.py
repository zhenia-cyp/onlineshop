from django.urls import path
from .views import catalog, product

app_name ='goods'

urlpatterns = [
    path('', catalog, name='index'),
    path('product/', product, name='product'),

]