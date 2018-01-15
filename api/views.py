from django.shortcuts import render
from urlshortener.serializer import shortenerSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import status
import shortuuid
from urlshortener.models import urls
from rest_framework.response import Response

base_url = 'http://localhost:8000/u/'


class shortenerListView(APIView):
    serializer_class = shortenerSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(urls.objects.all(), many = True)
        return Response(serializer.data)

class topEntryListView(APIView):
    serializer_class = shortenerSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(urls.objects.order_by('-count')[:10], many = True)
        return Response(serializer.data)

class createLink(APIView):
    # serializer_class = shortenerSerializer

    def get(self, request, format=None):
        serializer = shortenerSerializer(data=request.data)
        if data['alias']:
            alias = data['alias'].lower()
            data['link'] = base_url + str(alias)

        if serializer.is_valid():
            original = data['original'].lower()
            serializer.save()
            return Response(serializer.data)
        else:
             return Response({'message':'FORBIDEN'}, status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def teste(request):

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        print(data)

        if 'alias' in data: # Chamada com custom alias
            serializer = shortenerSerializer(data=data)
            alias = data['alias'].lower()
            data['link'] = base_url + str(alias)

            if serializer.is_valid():
                original = data['original'].lower()

                serializer.save()
                return JsonResponse(serializer.data)

            else:
                if serializer.errors['alias'][0] == 'urls with this alias already exists.':
                    errorDic = { "alias":alias,
                                 "err_code":"001",
                                 "description":"CUSTOM ALIAS ALREADY EXISTS" }

                    return JsonResponse(errorDic, status=status.HTTP_409_CONFLICT)

        else: # Chamada sem custom alias
            data['alias'] = 'Nothing'
            data['link'] = 'Nothing'
            serializer = shortenerSerializer(data=data)


            if serializer.is_valid():
                original = data['original'].lower()
                print('teste')
                if urls.objects.filter(custom = False).filter(original = original): # Caso link original já tenha sido submetido
                    data = urls.objects.filter(original = original).values()
                    print(data)
                    data = data[0]
                    dic = {
                        'original':data['original'],
                        'alias':data['alias'],
                        'link':data['link'],
                        'count':data['count'] }
                    return JsonResponse(dic)

                else:
                    data['alias'] = shortuuid.ShortUUID().random(length=6)
                    data['link'] = base_url+str(data['alias'])
                    serializer = shortenerSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data)


        return JsonResponse(serializer.errors, status=400)
