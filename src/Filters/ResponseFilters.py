# -*- coding: utf-8 -*-

from .ResponseFilter import ResponseFilter

from ..Request import Request
from ..Response import Response

__all__ = (
	'ResponseFilter',
)


class ResponseFilters(ResponseFilter):
	"""Response Filters"""

	def __init__(self, *args):
		self.filters = args
		return

	def __call__(self, request: Request, response: Response) -> Response:
		for f in self.filters:
			response = f(request, response)
		return response
