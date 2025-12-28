# -*- coding: utf-8 -*-

from ..Response import Response

from typing import Dict, Any

__all__ = (
	'ResponseBuffer'
)


class ResponseBuffer(Response):
	"""Response Buffer Class"""

	def __init__(
		self,
		buffer,
		size,
		format,
		charset=None,
		status=200,
		message='OK',
		headers: Dict[str, Any] = {} 
	):
		headers['Content-Length'] = size
		super(ResponseBuffer, self).__init__(
			status=status,
			message=message,
			headers=headers,
			body=buffer,
			format=format,
			charset=charset
		)
		return
