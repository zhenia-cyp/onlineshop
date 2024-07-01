from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.forms import UserRegistrationForm, ProfileForm
from django.contrib import auth
from django.contrib.auth import login
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from carts.models import Cart


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        session_key = self.request.session.session_key
        if user:
            login(self.request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Authorization'
        return context


class RegistrationView(View):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        return self.render_form(request, form)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            session_key = request.session.session_key
            auth.login(request, user)
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            return HttpResponseRedirect(reverse('main:index'))
        return self.render_form(request, form)

    def render_form(self, request, form):
        context = {
            'title': 'Home - Registration',
            'form': form
        }
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - My Profile'
        return context


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect(reverse_lazy('main:index'))


def users_cart(request):
    return render(request, 'users/users_cart.html')
