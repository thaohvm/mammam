from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView
from mammam import views

urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.png")),
    ),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("recipe/create", views.create, name="create"),
    path("recipe/<int:id>", views.view, name="view"),
]
