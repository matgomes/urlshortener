import logging

from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.services import UrlShorten, UrlRetrieve, UrlList

logger = logging.getLogger(__name__)


@api_view(['PUT'])
def shorten(request, url):

    custom_alias = request.query_params.get('custom_alias')

    service = UrlShorten(url, custom_alias, request.get_host(), request.start_time)

    return Response(service.shorten(), status.HTTP_201_CREATED)


@api_view(['GET'])
def retrieve(request, alias):

    original_url = UrlRetrieve(alias).retrieve()

    logger.info("Redirecting alias '{}' to original url '{}'".format(alias, original_url))

    return redirect(original_url)


@api_view(['GET'])
def most_accessed(request):

    limit = request.query_params.get('limit')

    service = UrlList(limit)

    return Response(service.get_most_accessed_urls(), status.HTTP_200_OK)

