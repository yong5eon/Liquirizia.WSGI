# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseRedirect'
)


class ResponseRedirect(Response):
	"""Response 302 Found with Redirect Class"""
	def __init__(self, url, body=None, format=None, charset=None):
		super(ResponseRedirect, self).__init__(
			status=302,
			message='Found',
			headers={
				'Content-Length': len(body) if body else 0,
				'Location': url,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return
