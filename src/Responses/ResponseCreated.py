# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseCreated'
)


class ResponseCreated(Response):
	"""Response 201 Created Class"""
	def __init__(self, body=None, format=None, charset=None):
		if body: body = SerializerHelper.Encode(body, format, charset)
		super(ResponseCreated, self).__init__(
			status=201,
			message='Created',
			headers={
				'Content-Length': len(body) if body else 0
			},
			body=body,
			format=format,
			charset=charset,
		)
		return
