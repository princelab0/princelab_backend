from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register_user/", views.register_user, name="register_user"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("user_profile/", views.user_profile, name="user_profile"),
]
