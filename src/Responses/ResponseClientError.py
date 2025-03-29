# -*- coding: utf-8 -*-

from ..Response import Response

from typing import Dict, Any

__all__ = (
	'ResponseBadRequest', # 400 Bad Request
	'ResponseUnauthorized', # 401 Unauthorized
	'ResponsePaymentRequired', # 402 Payment Required
	'ResponseForbidden', # 403 Forbidden
	'ResponseNotFound', # 404 Not Found
	'ResponseMethodNotAllowed', # 405 Method Not Allowed
	'ResponseNotAcceptable', # 406 Not Acceptable
	'ResponseProxyAuthenticationRequired', # 407 Proxy Authentication Required
	'ResponseRequestTimeout', # 408 Request Timeout
	'ResponseConflict', # 409 Conflict
	'ResponseGone', # 410 Gone
	'ResponseLengthRequired', # 411 Length Required
	'ResponsePreconditionFailed', # 412 Precondition Failed
	'ResponsePayloadTooLarge', # 413 Payload Too Large
	'ResponseURITooLong', # 414 URI Too Long
	'ResponseUnsupportedMediaType', # 415 Unsupported Media Type
	'ResponseRangeNotSatisfiable', # 416 Range Not Satisfiable
	'ResponseExpectationFailed', # 417 Expectation Failed
	# TODO : 418 I'm a teapot
	'ResponseMisdirectedRequest', # 421 Misdirected Request
	'ResponseUnprocessableEntity', # 422 Unprocessable Entity
	'ResponseLocked', # 423 Locked
	'ResponseFailedDependency', # 424 Failed Dependency
	'ResponseTooEarly', # 425 Too Early
	'ResponseUpgradeRequired', # 426 Upgrade Required
	'ResponseUnassigned', # 427 Unassigned
	'ResponsePreconditionRequired', # 428 Precondition Required
	'ResponseTooManyRequests', # 429 Too Many Requests
	'ResponseRequestHeaderFieldsTooLarge', # 431 Request Header Fields Too Large
	'ResponseUnavailableForLegalReasons', # 451 Unavailable For Legal Reasons
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


class ResponseUnauthorized(Response):
	"""Response 401 Unauthorized Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseBadRequest, self).__init__(
			status=401,
			message='Unauthorized',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponsePaymentRequired(Response):
	"""Response 402 Payment Required Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseBadRequest, self).__init__(
			status=402,
			message='Payment Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseForbidden(Response):
	"""Response 403 Forbidden Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseBadRequest, self).__init__(
			status=403,
			message='Forbidden',
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


class ResponseMethodNotAllowed(Response):
	"""Response 405 Method Not Allowed Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=405,
			message='Method Not Allowed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseNotAcceptable(Response):
	"""Response 406 Not Acceptable Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=406,
			message='Not Acceptable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseProxyAuthenticationRequired(Response):
	"""Response 407 Proxy Authentication Required Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=407,
			message='Proxy Authentication Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseRequestTimeout(Response):
	"""Response 408 Request Timeout Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=408,
			message='Request Timeout',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseConflict(Response):
	"""Response 409 Conflict Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=409,
			message='Conflict',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseGone(Response):
	"""Response 410 Gone Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=410,
			message='Gone',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseLengthRequired(Response):
	"""Response 411 Length Required Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=411,
			message='Length Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponsePreconditionFailed(Response):
	"""Response 412 Precondition Failed Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=412,
			message='Precondition Failed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponsePayloadTooLarge(Response):
	"""Response 413 Payload Too Large Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=413,
			message='Payload Too Large',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseURITooLong(Response):
	"""Response 414 URI Too Long Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=414,
			message='URI Too Long',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseUnsupportedMediaType(Response):
	"""Response 415 Unsupported Media Type Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=415,
			message='Unsupported Media Type',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseRangeNotSatisfiable(Response):
	"""Response 416 Range Not Satisfiable Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=416,
			message='Range Not Satisfiable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseExpectationFailed(Response):
	"""Response 417 Expectation Failed Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=417,
			message='Expectation Failed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return

# TODO : 418 I'm a teapot

class ResponseMisdirectedRequest(Response):
	"""Response 421 Misdirected Request Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=421,
			message='Misdirected Request',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseUnprocessableEntity(Response):
	"""Response 422 Unprocessable Entity Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=422,
			message='Unprocessable Entity',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseLocked(Response):
	"""Response 423 Locked Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=423,
			message='Locked',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseFailedDependency(Response):
	"""Response 424 Failed Dependency Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=424,
			message='Failed Dependency',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseTooEarly(Response):
	"""Response 425 Too Early Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=425,
			message='Too Early',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseUpgradeRequired(Response):
	"""Response 426 Upgrade Required Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=426,
			message='Upgrade Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseUnassigned(Response):
	"""Response 427 Unassigned Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=427,
			message='Unassigned',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponsePreconditionRequired(Response):
	"""Response 428 Precondition Required Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=428,
			message='Precondition Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseTooManyRequests(Response):
	"""Response 429 Too Many Requests Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=429,
			message='Too Many Requests',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseRequestHeaderFieldsTooLarge(Response):
	"""Response 431 Request Header Fields Too Large Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=431,
			message='Request Header Fields Too Large',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseUnavailableForLegalReasons(Response):
	"""Response 451 Unavailable For Legal Reasons Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super(ResponseNotFound, self).__init__(
			status=451,
			message='Unavailable For Legal Reasons',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return