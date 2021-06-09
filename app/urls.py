from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from text_flow import settings
from .views import HomePage, Login, Logout, SignIn, RoomView, CreateRoomView, send_circle, circle_list, delete_room, \
    stop_drawing, download_image

app_name = 'app'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('create_room/', login_required(CreateRoomView.as_view()), name='create_room'),
    path('ajax/send_circle/', send_circle, name='send_circle'),
    path('ajax/delete_room/', delete_room, name='delete_room'),
    path('ajax/stop_drawing/', stop_drawing, name='stop_drawing'),
    path('ajax/circle_list/', circle_list, name='circle_list'),
    path('room/<int:room_id>/', login_required(RoomView.as_view()), name='room'),
    path('room/download/<int:room_id>/', download_image, name='download_image'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', login_required(Logout.as_view()), name='logout'),
    path('signin/', SignIn.as_view(), name='signin'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)