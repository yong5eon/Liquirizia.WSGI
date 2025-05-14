# -*- coding: utf-8 -*-

from ..Response import Response
from ..Error import Error

__all__ = (
	'ResponseError'
)


class ResponseError(Response):
	"""Response Error Class"""
	def __init__(self, error: Error):
		super(ResponseError, self).__init__(
			status=error.status,
			message=error.message,
			headers=error.headers,
			body=error.body,
			format=error.format,
			charset=error.charset,
		)
		return
