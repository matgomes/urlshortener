import logging

from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)


class ExistingAliasApiException(APIException):

    def __init__(self, alias):

        logger.warning("Custom alias '{}' already exists".format(alias))

        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {
            "alias": alias,
            "err_code": "001",
            "description": "CUSTOM ALIAS ALREADY EXISTS"
        }


class AliasNotFoundApiException(APIException):

    def __init__(self, alias):

        logger.warning("Alias '{}' not found".format(alias))

        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = {
            "alias": alias,
            "err_code": "002",
            "description": "SHORTENED URL NOT FOUND"
        }


class MissingParamApiException(APIException):

    def __init__(self, missing_param):

        logger.warning("Missing query parameter '{}' on request".format(missing_param))

        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {
            "err_code": "003",
            "description": "Required String parameter '{}' is not present".format(missing_param)
        }
