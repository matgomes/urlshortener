from datetime import datetime

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from api.models import Url
from api.tests.helper.assertions import assert_valid_schema
from api import views


class ShortenViewTestCase(TestCase):

    factory = APIRequestFactory()

    def test_should_shorten(self):
        original_url = "http://test.com"
        alias = "alias"

        request = self.factory.put("/shorten/{}?custom_alias={}".format(original_url, alias))
        request.start_time = datetime.now()  # mocking middleware
        response = views.shorten(request, url=original_url)

        response_data = response.data

        assert_valid_schema(response_data, "shorten_response.json")
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response_data["alias"], alias)

    def test_should_not_shorten_existing_alias(self):

        original_url = "http://test.com"
        alias = "alias"

        Url(original_url=original_url, alias=alias).save()

        request = self.factory.put("/shorten/{}?custom_alias={}".format(original_url, alias))
        request.start_time = datetime.now()  # mocking middleware
        response = views.shorten(request, url=original_url)

        response_data = response.data

        assert_valid_schema(response_data, "exception_response.json")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response_data["err_code"], "001")
