# -*- coding: utf-8 -*-

from ..Response import Response
from ..Error import Error

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseError'
)


class ResponseError(Response):
	"""Response Error Class"""
	def __init__(self, error: Error, body: str = None, format: str = None, charset: str = None):
		super(ResponseError, self).__init__(
			status=error.status,
			message=error.message,
			headers={
				'Content-Length': len(body) if body else 0
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format='text/plain',
			charset='utf-8'
		)
		return
