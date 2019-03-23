from django.test import TestCase

from api.exceptions import AliasNotFoundApiException
from api.models import Url
from api.services import UrlRetrieve


class UrlRetrieveTestCase(TestCase):

    def setUp(self):
        self.original_url = "http://test.com"
        self.alias = "alias"

        Url(original_url=self.original_url, alias=self.alias, hits=0).save()

    def test_should_retrieve_original_url_and_increase_hits(self):

        url = UrlRetrieve(self.alias).retrieve()

        u = Url.objects.get(alias=self.alias)

        self.assertEquals(url, self.original_url)
        self.assertEquals(1, u.hits)

    def test_should_raise_alias_not_found_api_exception(self):

        with self.assertRaises(AliasNotFoundApiException):
            UrlRetrieve("dummy_alias").retrieve()
