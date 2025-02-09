# -*- coding: utf-8 -*-

from ..Response import Response
from ..Error import Error

from Liquirizia.Serializer import SerializerHelper

from typing import Dict, Any

__all__ = (
	'ResponseError'
)


class ResponseError(Response):
	"""Response Error Class"""
	def __init__(self, error: Error, body: str = None, format: str = None, charset: str = None, headers: Dict[str, Any] = {}):
		headers.update({'Content-Length': len(body) if body else 0})
		super(ResponseError, self).__init__(
			status=error.status,
			message=error.message,
			headers=headers,
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return
