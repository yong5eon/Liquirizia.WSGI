# -*- coding: utf-8 -*-

from .ResponseFilter import ResponseFilter

from ..Request import Request
from ..Response import Response

from typing import Tuple, Optional

__all__ = (
	'RequestFilters',
)


class RequestFilters(ResponseFilter):
	"""Request Fileters"""
	def __init__(self, *args):
		self.filters = args
		return

	def __call__(self, request: Request) -> Tuple[Request, Optional[Response]]:
		for f in self.filters:
			request, response = f(request)
			if response:
				return request, response
		return request, None
