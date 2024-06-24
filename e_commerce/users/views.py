from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.forms import UserRegistrationForm
from django.contrib import auth
from django.contrib.auth import login
from django.views import View


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
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
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
        return self.render_form(request, form)

    def render_form(self, request, form):
        context = {
            'title': 'Home - Registration',
            'form': form
        }
        return render(request, self.template_name, context)


def profile(request):
    context = {}
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))
    pass
