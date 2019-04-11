import logging

from xxhash import xxh32_hexdigest

from api.exceptions import ExistingAliasApiException, AliasNotFoundApiException
from api.models import Url
from api.responses import UrlShortenResponse
from api.serializers import UrlSerializer, UrlShortenResponseSerializer

logger = logging.getLogger(__name__)


class UrlShorten:

    serializer = UrlShortenResponseSerializer

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

        return self.get_response()

    def handle_shorten_with_custom_alias(self):

        logger.info("Shortening url '{}' with custom alias '{}'".format(self.original_url, self.alias))

        self.alias = self.alias.replace(" ", "")
        _, created = Url.objects.get_or_create(original_url=self.original_url, alias=self.alias)

        if not created:
            raise ExistingAliasApiException(self.alias)

        return self.get_response()

    def get_response(self):

        response = UrlShortenResponse(self.original_url, self.alias, self.host, self.start_time)

        return self.serializer(response).data


class UrlRetrieve:

    def __init__(self, alias):
        self.alias = alias

    def retrieve(self):

        logger.info("Retrieving original url for alias '{}'".format(self.alias))

        url = self.get_url_or_raise()
        url.hit()
        return url.original_url

    def get_url_or_raise(self):

        try:
            return Url.objects.get(alias=self.alias)

        except Url.DoesNotExist:
            raise AliasNotFoundApiException(self.alias)


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


def validate_url(original_url):
    url = original_url.replace(" ", "").replace("www.", "")

    if "//" not in url:
        url = "http://" + url

    return url


def validate_limit(limit):
    if isinstance(limit, str) and limit.isdigit():
        return int(limit)

    return 10
