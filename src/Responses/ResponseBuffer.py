# -*- coding: utf-8 -*-

from ..Response import Response

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
	):
		super(ResponseBuffer, self).__init__(
			status=status,
			message=message,
			headers={
				'Content-Length': size,
			},
			body=buffer,
			format=format,
			charset=charset
		)
		return
