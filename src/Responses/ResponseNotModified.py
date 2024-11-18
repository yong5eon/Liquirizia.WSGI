# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseNotModified'
)


class ResponseNotModified(Response):
	"""Reponse 304 Not Modified Class"""
	def __init__(self, body=None, format=None, charset=None):
		if body: body = SerializerHelper.Encode(body, format, charset)
		super(ResponseNotModified, self).__init__(
			status=304,
			message='Not Modified',
			headers={
				'Content-Length': len(body) if body else 0,
			},
			body=body,
			format=format,
			charset=charset,
		)
		return
