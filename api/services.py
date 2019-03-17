import logging
from datetime import datetime

from django.db.models import F
from xxhash import xxh32_hexdigest

from api.exceptions import ExistingAliasApiException, AliasNotFoundApiException
from api.models import Url
from api.serializers import UrlSerializer

logger = logging.getLogger(__name__)


def validate_url(original_url):
    url = original_url.replace(" ", "").replace("www.", "")

    if "//" not in url:
        url = "http://" + url

    return url


def validate_limit(limit):

    if isinstance(limit, str) and limit.isdigit():
        return int(limit)

    return 10


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

        logger.info("Shortening url '{}' with generated alias".format(self.original_url, self.alias))

        self.alias = xxh32_hexdigest(self.original_url)
        Url.objects.get_or_create(original_url=self.original_url, alias=self.alias)

        return self

    def handle_shorten_with_custom_alias(self):

        logger.info("Shortening url '{}' with custom alias '{}'".format(self.original_url, self.alias))

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

        logger.info("Retrieving original url for alias '{}'".format(self.alias))

        url = self.get_url_or_raise()
        url.update(hits=F("hits") + 1)
        return url.first().original_url

    def get_url_or_raise(self):

        url = Url.objects.filter(alias=self.alias)

        if not url:
            raise AliasNotFoundApiException(self.alias)

        return url


class UrlList:

    serializer = UrlSerializer

    def __init__(self, limit):

        self.limit = validate_limit(limit)

    def get_most_accessed_urls(self):

        if not self.limit:
            self.limit = 10

        logger.info("Getting most accessed urls with limit {}".format(self.limit))

        urls = Url.objects.all().order_by("-hits")[:self.limit]

        return self.serializer(urls, many=True).data

