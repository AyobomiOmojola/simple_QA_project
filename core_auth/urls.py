from django.urls import path, re_path
from . import views

app_name = "core_auth"


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]