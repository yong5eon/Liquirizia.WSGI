# -*- coding: utf-8 -*-

from ..Response import Response

from Liquirizia.Serializer import SerializerHelper

__all__ = (
	'ResponseMovePermanently',
	'ResponseFound',
	'ResponseNotModified',
)


class ResponseMovePermanently(Response):
	"""Response 301 Move Permanently Class"""
	def __init__(self, url, body=None, format=None, charset=None):
		super(ResponseMovePermanently, self).__init__(
			status=301,
			message='Move Permanently',
			headers={
				'Content-Length': len(body) if body else 0,
				'Location': url,
			},
			body=SerializerHelper.Encode(body, format, charset) if body else None,
			format=format,
			charset=charset,
		)
		return


class ResponseFound(Response):
	"""Response 302 Found Class"""
	def __init__(self, url, body=None, format=None, charset=None):
		super().__init__(
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
