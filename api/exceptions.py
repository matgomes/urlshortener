from rest_framework import status
from rest_framework.exceptions import APIException


class ExistingAliasApiException(APIException):

    def __init__(self, alias):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {
            "alias": alias,
            "err_code": "001",
            "description": "CUSTOM ALIAS ALREADY EXISTS"
        }


class AliasNotFoundApiException(APIException):

    def __init__(self):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = {
            "err_code": "002",
            "description": "SHORTENED URL NOT FOUND"
        }


class MissingParamApiException(APIException):

    def __init__(self, missing_param):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = {
            "err_code": "003",
            "description": "Required String parameter '{}' is not present".format(missing_param)
        }
