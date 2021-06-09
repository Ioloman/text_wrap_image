import os
import string
from random import choices
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files import File
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormView
from app.forms import RoomForm
from app.models import Room, RoomToUser, Circle
from app.image_text_wrap.wrap import get_image


def send_circle(request):
    """
    Создает круг, полученный из ajax запроса
    """
    if request.is_ajax() and request.method == 'POST':
        circle = Circle(
            x=request.POST.get('x'),
            y=request.POST.get('y'),
            r=request.POST.get('r'),
            room_id=request.POST.get('room_id')
        )
        circle.save()
        return JsonResponse({'status': 'Success'})


def delete_room(request):
    """
    Удаляет закрывает комнату по ajax запросу
    """
    if request.is_ajax() and request.method == 'POST':
        room = Room.objects.get(id=request.POST.get('room_id'))
        room.is_open = False
        room.save()
        return JsonResponse({'status': 'Success'})


def stop_drawing(request):
    """
    останавливает комнату и генерирует изображение
    """
    if request.is_ajax() and request.method == 'POST':
        room = Room.objects.get(id=request.POST.get('room_id'))
        room.is_drawing = False
        # получаем список кругов в необходимом для входа формате
        circles = room.circle_set.all()
        circle_list = [(circle.x, circle.y, circle.r) for circle in circles]
        # получаем изображение в формате PIL
        image = get_image(circle_list, room.text)
        # сохраняем в файл и загружаем в бд
        temp_name = room.name
        temp_name += str(choices(string.ascii_lowercase, k=5))
        temp_name += '.png'
        image.save(temp_name, format='PNG')
        room.image.save(room.name + '.png', File(open(temp_name, 'rb')))
        room.save()
        os.remove(temp_name)
        return JsonResponse({'status': 'Success'})


@login_required
def download_image(request, room_id):
    """
    возвращает картинку
    """
    room = Room.objects.get(id=room_id)
    return FileResponse(open(room.image.path, 'rb'))


def circle_list(request):
    """
    возвращает текущий список кругов по комнате
    """
    if request.is_ajax() and request.method == 'GET':
        return render(request, 'ajax\\circle_list.html', {'circles': Room.objects.get(id=request.GET.get('room_id')).circle_set.all().order_by('index')})


class HomePage(ListView):
    """
    Домашняя страница со списком комнат
    """
    template_name = 'html/index.html'
    context_object_name = 'rooms'
    queryset = Room.objects.filter(is_open=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RoomForm
        return context


class CreateRoomView(FormView):
    """
    Класс для создания комнаты
    """
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
    """
    Просмотр комнаты
    """
    model = Room
    template_name = 'html/room.html'
    context_object_name = 'room'
    pk_url_kwarg = 'room_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['host'] = get_object_or_404(RoomToUser, room=context['room'], is_host=True).user
        context['circles'] = context['room'].circle_set.all().order_by('index')
        context['users'] = context['room'].users.all()
        return context

    def get(self, request, *args, **kwargs):
        room = Room.objects.get(id=kwargs['room_id'])
        # если нет доступа в комнату, то переадресация на домашнюю
        if room.is_open is False or (room.is_drawing is False and request.user not in room.users.all()):
            return redirect('app:home')
        else:
            if request.user not in room.users.all():
                room.users.add(request.user, through_defaults={'is_host': False})
            return super().get(request, *args, *kwargs)


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




