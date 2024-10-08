# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseNotModified'
)


class ResponseNotModified(Response):
	"""Reponse 304 Not Modified Class"""
	def __init__(self, body=None, format=None, charset=None):
		super(ResponseNotModified, self).__init__(
			status=304,
			message='Not Modified',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return
