# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseOK'
)


class ResponseOK(Response):
	"""Response 200 OK Class"""
	def __init__(self, body=None, format=None, charset=None):
		super(ResponseOK, self).__init__(
			status=200,
			message='OK',
			headers={
				'Content-Length': len(body) if body else 0
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return
