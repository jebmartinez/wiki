from django.urls import path

from . import views

urlpatterns = [
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("randompage", views.randompage, name="randompage"),
    path("edit2", views.edit2, name="edit2"),
    path("<str:title>", views.entry, name="title"),
    path("", views.index, name="index")
]
