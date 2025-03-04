# -*- coding: utf-8 -*-

from ..Response import Response

from typing import Dict, Any

__all__ = (
	'ResponseInternalServerError', # 500
	'ResponseNotImplemented', # 501
	# TODO : 502 Bad Gateway
	'ResponseServiceUnavailable', # 503
	# TODO : 504 Gateway Timeout
	# TODO : 505 HTTP Version Not Supported
	# TODO : 506 Variant Also Negotiates
	# TODO : 507 Insufficient Storage
	# TODO : 508 Loop Detected
	# TODO : 510 Not Extended
	# TODO : 511 Network Authentication Required
)


class ResponseInternalServerError(Response):
	"""Response 500 Internal Server Error"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super().__init__(
			status=500,
			message='Internal Server Error',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseNotImplemented(Response):
	"""Response 501 Not Implemented"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super().__init__(
			status=501,
			message='Not Implemented',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseServiceUnavailable(Response):
	"""Response 503 Service Unavailable"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super().__init__(
			status=503,
			message='Service Unavailable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return
