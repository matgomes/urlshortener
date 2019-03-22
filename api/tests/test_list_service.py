from django.test import TestCase

from api.models import Url
from api.services import UrlList, validate_limit


class UrlLimitTestCase(TestCase):

    def setUp(self):
        self.original_url = "http://teste.com"
        self.alias = "alias"

    def test_should_get_10_most_accessed_urls_by_default(self):

        n = 15

        self.insert_urls(n)
        response = UrlList(limit=None).get_most_accessed_urls()

        self.assertEquals(len(response), 10)
        self.assertEquals(response[0]["hits"], n)
        self.assertEquals(response[1]["hits"], n - 1)

        self.assertEquals(response[0]["alias"], self.alias + str(n))
        self.assertEquals(response[0]["original_url"], self.original_url + str(n))

    def test_should_get_limited_most_accessed_urls(self):

        n = 5

        self.insert_urls(n)
        response = UrlList(limit="2").get_most_accessed_urls()

        self.assertEquals(len(response), 2)
        self.assertEquals(response[0]["hits"], n)
        self.assertEquals(response[1]["hits"], n - 1)

        self.assertEquals(response[0]["alias"], self.alias + str(n))
        self.assertEquals(response[0]["original_url"], self.original_url + str(n))

    def test_should_return_10_by_default(self):

        limit = validate_limit(None)
        self.assertEquals(limit, 10)

    def test_should_return_10_if_not_digit(self):

        limit = validate_limit("this_is_not_a_digit")
        self.assertEquals(limit, 10)

    def test_should_return_integer_instance(self):

        limit = validate_limit("2")
        self.assertEquals(limit, 2)

    def insert_urls(self, n):

        for i in range(n):
            Url(original_url=self.original_url + str(i+1), alias=self.alias + str(i+1), hits=i+1).save()
