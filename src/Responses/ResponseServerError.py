# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseInternalServerError',
	'ResponseNotImplemented',
	'ResponseServiceUnavailable',
)


class ResponseInternalServerError(Response):
	"""Response 500 Internal Server Error"""
	def __init__(self, body=None, format=None, charset=None):
		super().__init__(
			status=500,
			message='Internal Server Error',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return


class ResponseNotImplemented(Response):
	"""Response 501 Not Implemented"""
	def __init__(self, body=None, format=None, charset=None):
		super().__init__(
			status=501,
			message='Not Implemented',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return


class ResponseServiceUnavailable(Response):
	"""Response 503 Service Unavailable"""
	def __init__(self, body=None, format=None, charset=None):
		super().__init__(
			status=503,
			message='Service Unavailable',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return
