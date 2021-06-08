from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import HomePage, Login, Logout, SignIn

app_name = 'app'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', login_required(Logout.as_view()), name='logout'),
    path('signin/', SignIn.as_view(), name='signin'),
]