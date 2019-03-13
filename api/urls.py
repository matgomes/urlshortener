from django.urls import path

from api import views

urlpatterns = [
    path("shorten", views.shorten, name="shorten"),
    path("retrieve/<str:alias>", views.retrieve, name="retrieve"),
]
