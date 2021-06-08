from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import FormMixin, FormView, CreateView


class HomePage(TemplateView):
    template_name = 'html/index.html'


class Login(LoginView):
    template_name = 'html/login.html'
    authentication_form = AuthenticationForm


class Logout(LogoutView):
    pass


class SignIn(CreateView):
    form_class = UserCreationForm
    template_name = 'html/signin.html'
    success_url = reverse_lazy('app:home')

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)




