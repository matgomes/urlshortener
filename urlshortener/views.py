from django.shortcuts import render
from urlshortener import forms
import shortuuid
from urlshortener.models import urls
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect

from .serializer import shortenerSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

base_url = 'http://localhost:8000/u/'

def ifCustom(base, original, alias):
    link = base + str(alias)
    u = urls(original = original, alias = alias, link = link, custom = True)
    u.save()
    return link

def ifNotCustom(base, original, alias):
    alias = shortuuid.ShortUUID().random(length=6)
    link = base_url + str(alias)
    u = urls(original = original, alias = alias, link = link)
    u.save()
    return link

def index(request, error = False):
    top_entry = urls.objects.order_by('-count')[:10]

    form = forms.myForm()
    if request.method == 'POST':
        form = forms.myForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url'].lower()
            custom = form.cleaned_data['custom'].lower()

            if custom != '':
                try:
                    link = ifCustom(base_url, url, custom)
                    return render(request, 'urlshortener/result.html', {'link':link})
                except:
                    return render(request, 'urlshortener/result.html', {'link':'CUSTOM LINK JÁ EXISTENTE'})

            else:
                if urls.objects.filter(custom = False).filter(original = url):
                    link = urls.objects.get(custom = False, original = url).link
                    return render(request, 'urlshortener/result.html', {'link':link})
                else:
                    alias = shortuuid.ShortUUID().random(length=6)
                    link = ifNotCustom(base_url, url, alias)
                    return render(request, 'urlshortener/result.html', {'link':link})

    return render(request, 'urlshortener/index.html', {'form':form, 'entry':top_entry})


def redr(request, alias_key):
    key = alias_key
    link = urls.objects.get(alias = key)
    link.count += 1
    link.save()
    return HttpResponseRedirect(link.original)

class shortenerListView(APIView):
    serializer_class = shortenerSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(urls.objects.all(), many = True)
        return Response(serializer.data)

class shortenerView(APIView):
    def get(self, request, pk, format = None):
        print(pk)
        print('teste')
        custom = urls.objects.get(alias = pk).alias
        serializer = shortenerSerializer(custom)
        return Response(serializer.data)

class topEntryListView(APIView):
    serializer_class = shortenerSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(urls.objects.order_by('-count')[:10], many = True)
        return Response(serializer.data)
