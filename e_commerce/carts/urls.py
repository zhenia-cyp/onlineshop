from django.urls import path
from .views import CartAddView,  CartChangeView
from carts import views

app_name ='carts'

urlpatterns = [
    path('cart/add/', CartAddView.as_view(), name='cart_add'),
    path('cart/change/', CartChangeView.as_view(), name='cart_change'),
    path('cart/remove/', views.cart_remove, name='cart_remove'),
]