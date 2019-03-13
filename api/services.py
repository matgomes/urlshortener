from datetime import datetime

from django.db.models import F
from xxhash import xxh32_hexdigest

from api.exceptions import ExistingAliasApiException, AliasNotFoundApiException
from api.models import Url


def validate_url(original_url):
    url = original_url.replace(" ", "").replace("www.", "")

    if "//" not in url:
        url = "http://" + url

    return url


class UrlShorten:

    def __init__(self, original_url, custom_alias, host, start_time):
        self.original_url = validate_url(original_url)
        self.alias = custom_alias
        self.host = host
        self.start_time = start_time

    def shorten(self):
        if self.alias:
            return self.handle_shorten_with_custom_alias()

        return self.handle_shorten()

    def handle_shorten(self):
        self.alias = xxh32_hexdigest(self.original_url)
        Url.objects.get_or_create(original_url=self.original_url, alias=self.alias)

        return self

    def handle_shorten_with_custom_alias(self):

        self.alias = self.alias.replace(" ", "")
        existing, created = Url.objects.get_or_create(original_url=self.original_url, alias=self.alias)

        if created:
            return self

        if existing:
            raise ExistingAliasApiException(self.alias)

    def get_response(self):
        return {
            "original_url": self.original_url,
            "alias": self.alias,
            "url": '{}/retrieve/{}'.format(self.host, self.alias),
            "statistics": {
                "time_taken": int((datetime.now() - self.start_time).total_seconds() * 1000)
            }
        }


class UrlRetrieve:

    def __init__(self, alias):
        self.alias = alias

    def retrieve(self):
        url = self.get_url_or_raise()
        url.update(hits=F("hits") + 1)
        return url.first().original_url

    def get_url_or_raise(self):

        url = Url.objects.filter(alias=self.alias)

        if not url:
            raise AliasNotFoundApiException()

        return url
