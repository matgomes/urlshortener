from django.conf.urls import url
from django.contrib import admin
from urlshortener import views
from api import views as apiViews

urlpatterns = [
    url(r'^u/$', views.shortenerListView.as_view(), name='listview'),
    url(r'^top_entry/$', apiViews.topEntryListView.as_view(), name='listview'),
    url(r'^teste/$', apiViews.teste, name='showview'),
]
