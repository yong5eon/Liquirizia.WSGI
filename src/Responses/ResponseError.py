# -*- coding: utf-8 -*-

from ..Response import Response
from ..Error import Error

__all__ = (
	'ResponseError'
)


class ResponseError(Response):
	"""Response Error Class"""
	def __init__(self, error: Error):
		headers = error.headers if error.headers else {}
		body = None
		format = None
		charset = None
		if error.body:
			body = error.body
			format = error.format
			charset = error.charset
		else:
			body = error.traceback.encode('utf-8')
			format = 'text/plain'
			charset = 'utf-8'
		super(ResponseError, self).__init__(
			status=error.status,
			message=error.message,
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return
