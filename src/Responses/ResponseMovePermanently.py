# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseMovePermanently'
)


class ResponseMovePermanently(Response):
	"""Response 301 Move Permanently Class"""
	def __init__(self, url, body=None, format=None, charset=None):
		if body: body = SerializerHelper.Encode(body, format, charset)
		super(ResponseMovePermanently, self).__init__(
			status=301,
			message='Move Permanently',
			headers={
				'Content-Length': len(body) if body else 0,
				'Location': url,
			},
			body=body,
			format=format,
			charset=charset,
		)
		return
