from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm
app_name = "users"
urlpatterns = [
    path("login/",auth_views.LoginView.as_view(template_name ="user/login.html",authentication_form = CustomAuthenticationForm),name = 'login'),
    path("logout/",auth_views.LogoutView.as_view(next_page = "users:login"),name ="logout"),
    path("register/",views.register_view,name = "register"),
    path("profile/",views.profile_view,name = 'profile'),
]
