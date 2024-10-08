# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Filters import RequestFilter
from Liquirizia.WSGI import Request, Response

__all__ = (
    'ToJPEG'
)


class ToJPEG(RequestFilter):
    def run(self, request: Request) -> Request:
        request.path = '{}.jpg'.format(request.path)
        return request, None
