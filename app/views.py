from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import FormMixin, CreateView, FormView

from app.forms import RoomForm
from app.models import Room, RoomToUser


class HomePage(ListView):
    template_name = 'html/index.html'
    context_object_name = 'rooms'
    queryset = Room.objects.filter(is_open=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RoomForm
        return context


class CreateRoomView(FormView):
    form_class = RoomForm

    def form_valid(self, form):
        room = Room(name=form.cleaned_data['name'], text=form.cleaned_data['text'])
        room.save()
        room.users.add(self.request.user, through_defaults={'is_host': True})
        self.kwargs['room_id'] = room.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('app:room', args=[self.kwargs['room_id']])


class RoomView(DetailView):
    model = Room
    template_name = 'html/room.html'
    context_object_name = 'room'
    pk_url_kwarg = 'room_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['host'] = get_object_or_404(RoomToUser, user=self.request.user, room=context['room'], is_host=True)
        return context


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




