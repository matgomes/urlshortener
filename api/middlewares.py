from datetime import datetime


class StatsMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.start_time = datetime.now()
        return self.get_response(request)
