from django.urls import path
from .views import LoginView, RegistrationView, ProfileView, LogoutView
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/', views.users_cart, name='users_cart'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
