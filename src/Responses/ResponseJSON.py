# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

from typing import Dict, Any

__all__ = (
	'ResponseJSON'
)


class ResponseJSON(Response):
	"""Response JSON Class"""
	def __init__(self, body, format='application/json', charset='utf-8', status=200, message='OK', headers: Dict[str, Any ]= {}):
		headers.update({'Content-Length': len(body)})
		body = SerializerHelper.Encode(body, format, charset)
		super().__init__(
			status=status,
			message=message,
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return
