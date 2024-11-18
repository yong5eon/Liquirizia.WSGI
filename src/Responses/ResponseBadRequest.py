# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseBadRequest'
)


class ResponseBadRequest(Response):
	"""Response 400 Bad Request Class"""
	def __init__(self, body=None, format=None, charset=None):
		if body: body = SerializerHelper.Encode(body, format, charset)
		super(ResponseBadRequest, self).__init__(
			status=400,
			message='Bad Request',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=body,
			format=format,
			charset=charset,
		)
		return
