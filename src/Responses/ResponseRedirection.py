# -*- coding: utf-8 -*-

from ..Response import Response

from typing import Dict, Any

__all__ = (
	# TODO : 300 Multiple Choices
	'ResponseMovePermanently', # 301
	'ResponseFound', # 302
	# TODO : 303 See Other
	'ResponseNotModified', # 304
	# TODO : 305 Use Proxy
	# TODO : 306 Switch Proxy
	# TODO : 307 Temporary Redirect
	# TODO : 308 Permanent Redirect
)


class ResponseMovePermanently(Response):
	"""Response 301 Move Permanently Class"""
	def __init__(self, url, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		headers.update({
			'Location': url,
		})
		super(ResponseMovePermanently, self).__init__(
			status=301,
			message='Move Permanently',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseFound(Response):
	"""Response 302 Found Class"""
	def __init__(self, url, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		headers.update({
			'Location': url,
		})
		super().__init__(
			status=302,
			message='Found',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseNotModified(Response):
	"""Reponse 304 Not Modified Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotModified, self).__init__(
			status=304,
			message='Not Modified',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return
