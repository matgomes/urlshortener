
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from api import views
from api.models import Url
from api.tests.helper.assertions import assert_valid_schema


class RetrieveViewTestCase(TestCase):

    factory = APIRequestFactory()

    def test_should_retrieve(self):

        original_url = "http://test.com"
        alias = "alias"

        Url(original_url=original_url, alias=alias).save()

        request = self.factory.get("/retrieve")
        response = views.retrieve(request, alias)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, original_url)

    def test_should_not_retrieve(self):

        request = self.factory.get("/retrieve")
        response = views.retrieve(request, "dummy_alias")

        response_data = response.data

        assert_valid_schema(response_data, "exception_response.json")
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response_data["err_code"], "002")

