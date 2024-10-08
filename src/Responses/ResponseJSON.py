# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseJSON'
)


class ResponseJSON(Response):
	"""Response JSON Class"""
	def __init__(self, body, format='application/json', charset='utf-8', status=200, message='OK', headers: dict = None):
		body = SerializerHelper.Encode(body, format, charset)
		props={
			'Content-Length': len(body)
		}
		props.update(headers if headers else {})
		super().__init__(
			status=status,
			message=message,
			headers=props,
			body=body,
			format=format,
			charset=charset,
		)
		return
