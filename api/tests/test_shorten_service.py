from datetime import datetime

from django.test import TestCase
from xxhash.cpython import xxh32_hexdigest

from api.exceptions import ExistingAliasApiException
from api.models import Url
from api.services import UrlShorten, validate_url


class UrlShortenTestCase(TestCase):

    def setUp(self):
        self.host = "http://host.com"
        self.start_time = datetime.now()
        self.original_url = "http://teste.com"
        self.alias = "alias"

    def test_should_create_url_with_custom_alias(self):

        response = UrlShorten(self.original_url, self.alias, self.host, self.start_time).shorten()

        u = Url.objects.get(alias=self.alias)

        expected_url = "{}/retrieve/{}".format(self.host, self.alias)

        self.assertEquals(response['alias'], self.alias)
        self.assertEquals(response['original_url'], self.original_url)
        self.assertEquals(response['url'], expected_url)
        self.assertIsInstance(response['statistics']['time_taken'], int)

        self.assertEquals(u.alias, self.alias)
        self.assertEquals(u.original_url, self.original_url)
        self.assertEquals(u.hits, 0)

    def test_should_raise_existing_alias_api_exception(self):

        Url(alias=self.alias, original_url=self.original_url).save()

        with self.assertRaises(ExistingAliasApiException):
            UrlShorten(self.original_url, self.alias, self.host, self.start_time).shorten()

    def test_should_create_url_with_generated_alias(self):

        response = UrlShorten(self.original_url, None, self.host, self.start_time).shorten()

        self.alias = xxh32_hexdigest(self.original_url)

        u = Url.objects.get(alias=self.alias)

        expected_url = "{}/retrieve/{}".format(self.host, self.alias)

        self.assertEquals(response['alias'], self.alias)
        self.assertEquals(response['original_url'], self.original_url)
        self.assertEquals(response['url'], expected_url)
        self.assertIsInstance(response['statistics']['time_taken'], int)

        self.assertEquals(u.alias, self.alias)
        self.assertEquals(u.original_url, self.original_url)
        self.assertEquals(u.hits, 0)

    def test_should_remove_www(self):

        url = "http://www.teste.com"
        expected_url = url.replace("www.", "")

        validated_url = validate_url(url)

        self.assertEquals(validated_url, expected_url)

    def test_should_add_http_if_empty_schema(self):

        url = "teste.com"
        expected_url = "http://" + url

        validated_url = validate_url(url)

        self.assertEquals(validated_url, expected_url)

    def test_should_not_add_http_if_has_schema(self):

        url = "https://teste.com"

        validated_url = validate_url(url)

        self.assertEquals(validated_url, url)