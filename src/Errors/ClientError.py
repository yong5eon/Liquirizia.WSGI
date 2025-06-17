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
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(BadRequestError, self).__init__(
			400,
			'Bad Request',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class UnauthorizedError(Error):
	"""Unauthorized Error Class, 401"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(UnauthorizedError, self).__init__(
			401,
			'Unauthorized',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class PaymentRequiredError(Error):
	"""PaymentRequired Error Class, 402"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(PaymentRequiredError, self).__init__(
			402,
			'Payment Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class ForbiddenError(Error):
	"""Forbidden Error Class, 403"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(ForbiddenError, self).__init__(
			403,
			'Forbidden',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class NotFoundError(Error):
	"""Not Found Error Class, 404"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(NotFoundError, self).__init__(
			404,
			'Not Found',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class MethodNotAllowedError(Error):
	"""Method Not Allowed Error Class, 405"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(MethodNotAllowedError, self).__init__(
			405,
			'Method Not Allowed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class NotAcceptableError(Error):
	"""Not Acceptable Error Class, 406"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(NotAcceptableError, self).__init__(
			406,
			'Not Acceptable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class ProxyAuthenticationRequiredError(Error):
	"""Proxy Authentication Required Error Class, 407"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(ProxyAuthenticationRequiredError, self).__init__(
			407,
			'Proxy Authentication Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class RequestTimeoutError(Error):
	"""Request Timeout Error Class, 408"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(RequestTimeoutError, self).__init__(
			408,
			'Request Timeout',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class ConflictError(Error):
	"""Conflict Error Class, 409"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(ConflictError, self).__init__(
			409,
			'Conflict',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class GoneError(Error):
	"""Gone Error Class, 410"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(GoneError, self).__init__(
			410,
			'Gone',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class LengthRequiredError(Error):
	"""Length Required Error Class, 411"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(LengthRequiredError, self).__init__(
			411,
			'Length Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class UnsupportedMediaTypeError(Error):
	"""Unsupported Media Type Error Class, 415"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(UnsupportedMediaTypeError, self).__init__(
			415,
			'Unsupported Media Type',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class PreconditionFailedError(Error):
	"""Precondition Failed Error Class, 412"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(PreconditionFailedError, self).__init__(
			412,
			'Precondition Failed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class PayloadTooLargeError(Error):
	"""Payload Too Large Error Class, 413"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(PayloadTooLargeError, self).__init__(
			413,
			'Payload Too Large',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class URITooLongError(Error):
	"""URI Too Long Error Class, 414"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(URITooLongError, self).__init__(
			414,
			'URI Too Long',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class RangeNotSatisfiableError(Error):
	"""Range Not Satisfiable Error Class, 416"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(RangeNotSatisfiableError, self).__init__(
			416,
			'Range Not Satisfiable',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class ExpectationFailedError(Error):
	"""Expectation Failed Error Class, 417"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(ExpectationFailedError, self).__init__(
			417,
			'Expectation Failed',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class UnprocessableEntityError(Error):
	"""Unprocessable Entity Error Class, 422"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(UnprocessableEntityError, self).__init__(
			422,
			'Unprocessable Entity',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class TooEarlyError(Error):
	"""Too Early Error Class, 425"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(TooEarlyError, self).__init__(
			425,
			'Too Early',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class UpgradeRequiredError(Error):
	"""Upgrade Required Error Class, 426"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(UpgradeRequiredError, self).__init__(
			426,
			'Upgrade Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class TooManyRequestsError(Error):
	"""Too Many Requests Error Class, 429"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(TooManyRequestsError, self).__init__(
			429,
			'Too Many Requests',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class PreconditionRequiredError(Error):
	"""Precondition Required Error Class, 428"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(PreconditionRequiredError, self).__init__(
			428,
			'Precondition Required',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return


class RequestHeaderFieldsTooLargeError(Error):
	"""Request Header Fields Too Large Error Class, 431"""
	def __init__(
		self,
		headers: Dict[str, Any] = None,
		body: bytes = None,
		format: str = None,
		charset: str = None,
		reason: str = None,
		error: BaseException = None,
		extra: Any = None,
	):
		super(RequestHeaderFieldsTooLargeError, self).__init__(
			431,
			'Request Header Fields Too Large',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
			reason=reason,
			error=error,
			extra=extra,
		)
		return
