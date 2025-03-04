# -*- coding: utf-8 -*-

from ..Response import Response

from typing import Dict, Any

__all__ = (
	'ResponseBadRequest', # 400
	# TODO : 401 Unauthorized
	# TODO : 402 Payment Required
	# TODO : 403 Forbidden
	'ResponseNotFound', # 404
	# TODO : 405 Method Not Allowed
	# TODO : 406 Not Acceptable
	# TODO : 407 Proxy Authentication Required
	# TODO : 408 Request Timeout
	# TODO : 409 Conflict
	# TODO : 410 Gone
	# TODO : 411 Length Required
	# TODO : 412 Precondition Failed
	# TODO : 413 Payload Too Large
	# TODO : 414 URI Too Long
	# TODO : 415 Unsupported Media Type
	# TODO : 416 Range Not Satisfiable
	# TODO : 417 Expectation Failed
	# TODO : 418 I'm a teapot
	# TODO : 421 Misdirected Request
	# TODO : 422 Unprocessable Entity
	# TODO : 423 Locked
	# TODO : 424 Failed Dependency
	# TODO : 425 Too Early
	# TODO : 426 Upgrade Required
	# TODO : 428 Precondition Required
	# TODO : 429 Too Many Requests
	# TODO : 431 Request Header Fields Too Large
	# TODO : 451 Unavailable For Legal Reasons
)


class ResponseBadRequest(Response):
	"""Response 400 Bad Request Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseBadRequest, self).__init__(
			status=400,
			message='Bad Request',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseNotFound(Response):
	"""Response 404 Not Found Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=404,
			message='Not Found',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return
