# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseBadRequest',
	'ResponseNotFound',
)


class ResponseBadRequest(Response):
	"""Response 400 Bad Request Class"""
	def __init__(self, body=None, format=None, charset=None):
		super(ResponseBadRequest, self).__init__(
			status=400,
			message='Bad Request',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return


class ResponseNotFound(Response):
	"""Response 404 Not Found Class"""
	def __init__(self, body=None, format=None, charset=None):
		super(ResponseNotFound, self).__init__(
			status=404,
			message='Not Found',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return
