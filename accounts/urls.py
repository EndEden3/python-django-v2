from django.urls import path

from .views import signup_view, signin_view, logout_view


urlpatterns = [
    path("logup/", signup_view, name="signup"),
    path("login/", signin_view, name="signin"),
    path("logout/", logout_view, name="logout"),
]