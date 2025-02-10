# -*- coding: utf-8 -*-

from ..Error import Error

from typing import Dict, Any

__all__ = (
	'BadRequestError', # 400
	'UnauthorizedError', # 401
	'PaymentRequiredError', # 402
	'ForbiddenError', # 403
	'NotFoundError', # 404
	'MethodNotAllowedError', # 405
	'NotAcceptableError', # 406
	'ProxyAuthenticationRequiredError', # 407
	'RequestTimeoutError', # 408
	'ConflictError', # 409
	'GoneError', # 410
	'LengthRequiredError', # 411
	'PreconditionFailedError', # 412
	'PayloadTooLargeError', # 413
	'URITooLongError', # 414
	'UnsupportedMediaTypeError', # 415
	'RangeNotSatisfiableError', # 416
	'ExpectationFailedError', # 417
	'UnprocessableEntityError', # 422
	'TooEarlyError', # 425
	'UpgradeRequiredError', # 426
	'PreconditionRequiredError', # 428
	'TooManyRequestsError', # 429
	'RequestHeaderFieldsTooLargeError', # 431
)


class BadRequestError(Error):
	"""Bad Request Class, 400"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(BadRequestError, self).__init__(
			reason,
			400,
			'Bad Request',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class UnauthorizedError(Error):
	"""Unauthorized Error Class, 401"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(UnauthorizedError, self).__init__(
			reason,
			401,
			'Unauthorized',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class PaymentRequiredError(Error):
	"""PaymentRequired Error Class, 402"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(PaymentRequiredError, self).__init__(
			reason,
			402,
			'Payment Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class ForbiddenError(Error):
	"""Forbidden Error Class, 403"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(ForbiddenError, self).__init__(
			reason,
			403,
			'Forbidden',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class NotFoundError(Error):
	"""Not Found Error Class, 404"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(NotFoundError, self).__init__(
			reason,
			404,
			'Not Found',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class MethodNotAllowedError(Error):
	"""Method Not Allowed Error Class, 405"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(MethodNotAllowedError, self).__init__(
			reason,
			405,
			'Method Not Allowed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class NotAcceptableError(Error):
	"""Not Acceptable Error Class, 406"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(NotAcceptableError, self).__init__(
			reason,
			406,
			'Not Acceptable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class ProxyAuthenticationRequiredError(Error):
	"""Proxy Authentication Required Error Class, 407"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(ProxyAuthenticationRequiredError, self).__init__(
			reason,
			407,
			'Proxy Authentication Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class RequestTimeoutError(Error):
	"""Request Timeout Error Class, 408"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(RequestTimeoutError, self).__init__(
			reason,
			408,
			'Request Timeout',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class ConflictError(Error):
	"""Conflict Error Class, 409"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(ConflictError, self).__init__(
			reason,
			409,
			'Conflict',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class GoneError(Error):
	"""Gone Error Class, 410"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(GoneError, self).__init__(
			reason,
			410,
			'Gone',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class LengthRequiredError(Error):
	"""Length Required Error Class, 411"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(LengthRequiredError, self).__init__(
			reason,
			411,
			'Length Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class UnsupportedMediaTypeError(Error):
	"""Unsupported Media Type Error Class, 415"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(UnsupportedMediaTypeError, self).__init__(
			reason,
			415,
			'Unsupported Media Type',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class PreconditionFailedError(Error):
	"""Precondition Failed Error Class, 412"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(PreconditionFailedError, self).__init__(
			reason,
			412,
			'Precondition Failed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class PayloadTooLargeError(Error):
	"""Payload Too Large Error Class, 413"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(PayloadTooLargeError, self).__init__(
			reason,
			413,
			'Payload Too Large',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class URITooLongError(Error):
	"""URI Too Long Error Class, 414"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(URITooLongError, self).__init__(
			reason,
			414,
			'URI Too Long',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class RangeNotSatisfiableError(Error):
	"""Range Not Satisfiable Error Class, 416"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(RangeNotSatisfiableError, self).__init__(
			reason,
			416,
			'Range Not Satisfiable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class ExpectationFailedError(Error):
	"""Expectation Failed Error Class, 417"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(ExpectationFailedError, self).__init__(
			reason,
			417,
			'Expectation Failed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class UnprocessableEntityError(Error):
	"""Unprocessable Entity Error Class, 422"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(UnprocessableEntityError, self).__init__(
			reason,
			422,
			'Unprocessable Entity',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class TooEarlyError(Error):
	"""Too Early Error Class, 425"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(TooEarlyError, self).__init__(
			reason,
			425,
			'Too Early',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class UpgradeRequiredError(Error):
	"""Upgrade Required Error Class, 426"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(UpgradeRequiredError, self).__init__(
			reason,
			426,
			'Upgrade Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class TooManyRequestsError(Error):
	"""Too Many Requests Error Class, 429"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(TooManyRequestsError, self).__init__(
			reason,
			429,
			'Too Many Requests',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class PreconditionRequiredError(Error):
	"""Precondition Required Error Class, 428"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(PreconditionRequiredError, self).__init__(
			reason,
			428,
			'Precondition Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return


class RequestHeaderFieldsTooLargeError(Error):
	"""Request Header Fields Too Large Error Class, 431"""
	def __init__(
		self,
		reason: str,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		error: BaseException = None,
	):
		super(RequestHeaderFieldsTooLargeError, self).__init__(
			reason,
			431,
			'Request Header Fields Too Large',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			error=error,
		)
		return
