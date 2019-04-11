
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from api.models import Url
from api.tests.helper.assertions import assert_valid_schema
from api import views


class RetrieveViewTestCase(TestCase):

    factory = APIRequestFactory()

    def setUp(self):
        self.original_url = "http://test.com"
        self.alias = "alias"

    def test_should_get_most_accessed(self):

        self.insert_urls(15)

        request = self.factory.get("/most_accessed")
        response = views.most_accessed(request)

        response_data = response.data

        assert_valid_schema(response_data, 'list_response.json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response_data), 10)

    def test_should_get_most_accessed_by_limit_param(self):

        self.insert_urls(15)

        limit = 5

        request = self.factory.get("/most_accessed?limit={}".format(limit))
        response = views.most_accessed(request)

        response_data = response.data

        assert_valid_schema(response_data, 'list_response.json')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response_data), limit)

    def test_should_get_most_accessed_empty(self):

        request = self.factory.get("/most_accessed")
        response = views.most_accessed(request)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 0)

    def insert_urls(self, n):

        for i in range(n):
            Url(original_url=self.original_url + str(i+1), alias=self.alias + str(i+1), hits=i+1).save()