# -*- coding: utf-8 -*-

from ..Response import Response
from .ResponseFilter import ResponseFilter

__all__ = (
	'ResponseFilter',
)


class ResponseFilters(ResponseFilter):
	"""Response Filters"""

	def __init__(self, *args):
		self.filters = args
		return

	def run(self, response: Response) -> Response:
		for f in self.filters:
			response = f.run(response)
		return response

