from datetime import datetime


class ApiExceptionResponse(object):

    def __init__(self, err_code, description, alias=None):
        self.description = description
        self.err_code = err_code
        self.alias = alias


class UrlShortenResponse(object):

    def __init__(self, original_url, alias, host, start_time):
        self.original_url = original_url
        self.alias = alias
        self.url = '{}/retrieve/{}'.format(host, alias)
        self.statistics = get_time_taken(start_time)


def get_time_taken(start_time):
    return {
        "time_taken": int((datetime.now() - start_time).total_seconds() * 1000)
    }

