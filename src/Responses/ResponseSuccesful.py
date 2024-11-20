# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseOK', # 200
	'ResponseCreated', # 201
	'ResponseAccepted', # 202
	'ResponseNoContent', # 204
)


class ResponseOK(Response):
	"""Response 200 OK Class"""
	def __init__(self, body=None, format=None, charset=None):
		if body: body = SerializerHelper.Encode(body, format, charset)
		super().__init__(
			status=200,
			message='OK',
			headers={
				'Content-Length': len(body) if body else 0
			},
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseCreated(Response):
	"""Response 201 Created Class"""
	def __init__(self, body=None, format=None, charset=None):
		super().__init__(
			status=201,
			message='Created',
			headers={
				'Content-Length': len(body) if body else 0
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return


class ResponseAccepted(Response):
	"""Response 202 Accepted Class"""
	def __init__(self, body=None, format=None, charset=None):
		super().__init__(
			status=202,
			message='Accepted',
			headers={
				'Content-Length': len(body) if body else 0
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return


class ResponseNoContent(Response):
	"""Response 204 No Content Class"""
	def __init__(self, body=None, format=None, charset=None):
		super().__init__(
			status=204,
			message='No Content',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return
