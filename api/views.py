from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.exceptions import MissingParamApiException
from api.services import UrlShorten, UrlRetrieve, get_top10


@api_view(['PUT'])
def shorten(request):

    params = request.query_params
    url = params.get('url')
    custom_alias = params.get('custom_alias')

    if not url:
        raise MissingParamApiException(missing_param='url')

    service = UrlShorten(url, custom_alias, request.get_host(), request.start_time).shorten()

    return Response(service.get_response(), status.HTTP_201_CREATED)


@api_view(['GET'])
def retrieve(request, alias):

    return redirect(UrlRetrieve(alias).retrieve())


@api_view(['GET'])
def top10(request):

    return Response(get_top10(), status.HTTP_200_OK)

