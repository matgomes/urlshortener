from django.urls import path

from api import views

urlpatterns = [
    path("shorten/<str:url>", views.shorten, name="shorten"),
    path("retrieve/<str:alias>", views.retrieve, name="retrieve"),
    path("most_accessed", views.most_accessed, name="most_accessed"),
]
