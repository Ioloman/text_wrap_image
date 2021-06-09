from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from text_flow import settings
from .views import HomePage, Login, Logout, SignIn, RoomView, CreateRoomView

app_name = 'app'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('create_room/', login_required(CreateRoomView.as_view()), name='create_room'),
    path('room/<int:room_id>/', login_required(RoomView.as_view()), name='room'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', login_required(Logout.as_view()), name='logout'),
    path('signin/', SignIn.as_view(), name='signin'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)