from django.urls import path
from .views import CartAddView
from carts import views

app_name ='carts'

urlpatterns = [
    path('cart/add/', CartAddView.as_view(), name='cart_add'),
    path('cart/change/', views.cart_change, name='cart_change'),
    path('cart/remove/', views.cart_remove, name='cart_remove'),

]