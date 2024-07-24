from django.urls import path
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_piano", views.add_piano, name="add_piano"),
    path("add_piano1", views.add_piano1, name="add_piano1"),
    path("add_piano2", views.add_piano2, name="add_piano2"),
    path("piano_detail/<int:piano_id>", views.piano_detail, name="piano_detail"),
    path("vote/<int:piano_id>", views.vote, name="vote"),
    path("delete_piano/<int:piano_id>", views.delete_piano, name="delete_piano"),
]