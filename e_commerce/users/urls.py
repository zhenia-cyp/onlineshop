from django.urls import path
from users import views
from .views import LoginView, RegistrationView, ProfileView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', views.logout, name='logout'),
]
