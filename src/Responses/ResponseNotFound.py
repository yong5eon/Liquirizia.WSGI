# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseNotFound'
)


class ResponseNotFound(Response):
	"""Response 404 Not Found Class"""

	def __init__(self, body=None, format=None, charset=None):
		if body: body = SerializerHelper.Encode(body, format, charset)
		super(ResponseNotFound, self).__init__(
			status=404,
			message='Not Found',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=body,
			format=format,
			charset=charset,
		)
		return
