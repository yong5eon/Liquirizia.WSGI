# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestFilter
from Liquirizia.WSGI import Request, Response

from typing import Tuple, Optional

__all__ = (
    'ToJPEG'
)


class ToJPEG(RequestFilter):
    def __call__(self, request: Request) -> Tuple[Request, Optional[Response]]:
        request.path = '{}.jpg'.format(request.path)
        return request, None
