# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseHTML'
)


class ResponseHTML(Response):
	"""Response HTML Class"""
	def __init__(self, body, format='text/html', charset='utf-8', status=200, message='OK'):
		body = SerializerHelper.Encode(body, format, charset)
		super(ResponseHTML, self).__init__(
			status=status,
			message=message,
			headers={
				'Content-Length': len(body)
			},
			body=body,
			format=format,
			charset=charset,
		)
		return
