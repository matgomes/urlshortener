import logging

from rest_framework import status
from rest_framework.exceptions import APIException

from api.responses import ApiExceptionResponse
from api.serializers import ExceptionDetailSerializer

logger = logging.getLogger(__name__)

serializer = ExceptionDetailSerializer


class ExistingAliasApiException(APIException):

    def __init__(self, alias):

        logger.warning("Custom alias '{}' already exists".format(alias))

        response = ApiExceptionResponse(alias=alias,
                                        err_code="001",
                                        description="CUSTOM ALIAS ALREADY EXISTS")

        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = serializer(response).data


class AliasNotFoundApiException(APIException):

    def __init__(self, alias):

        logger.warning("Alias '{}' not found".format(alias))

        response = ApiExceptionResponse(alias=alias,
                                        err_code="002",
                                        description="SHORTENED URL NOT FOUND")

        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = serializer(response).data


class MissingParamApiException(APIException):

    def __init__(self, missing_param):

        logger.warning("Missing query parameter '{}' on request".format(missing_param))

        response = ApiExceptionResponse(err_code="003",
                                        description="REQUIRED PARAMETER '{}' IS NOT PRESENT".format(missing_param))

        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = serializer(response).data
