# -*- coding: utf-8 -*-

from ..Response import Response
from ..Error import Error

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseError'
)


class ResponseError(Response):
	"""Response Error Class"""
	def __init__(self, error: Error):
		body = SerializerHelper.Encode(str(error), format='text/plain', charset='utf-8')
		super(ResponseError, self).__init__(
			status=error.status,
			message=error.message,
			headers={
				'Content-Length': len(body)
			},
			body=body,
			format='text/plain',
			charset='utf-8'
		)
		return
