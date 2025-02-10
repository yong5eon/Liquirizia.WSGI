# -*- coding: utf-8 -*-

from .ClientError import ( # client error
	BadRequestError, # 400
	UnauthorizedError, # 401
	PaymentRequiredError, # 402
	ForbiddenError, # 403
	NotFoundError, # 404
	MethodNotAllowedError, # 405
	NotAcceptableError, # 406
	ProxyAuthenticationRequiredError, # 407
	RequestTimeoutError, # 408
	ConflictError, # 409
	GoneError, # 410
	LengthRequiredError, # 411
	PreconditionFailedError, # 412
	PayloadTooLargeError, # 413
	URITooLongError, # 414
	UnsupportedMediaTypeError, # 415
	RangeNotSatisfiableError, # 416
	ExpectationFailedError, # 417
	# TODO : 418 I'm a teapot
	UnprocessableEntityError,  # 422
	TooEarlyError, # 425
	UpgradeRequiredError,  # 426
	PreconditionRequiredError, # 428
	TooManyRequestsError,  # 429
	RequestHeaderFieldsTooLargeError, # 431
	# TODO : 451 Unavailable For Legal Reasons
)
from .ServerError import ( # server error
	InternalServerError, # 500
	NotImplementedError, # 501
	# TODO : 502 Bad Gateway
	ServiceUnavailableError,  # 503
	# TODO : 504 Gateway Timeout
	VersionNotSupportedError, # 505
	# TODO : 506 Variant Also Negotiates
	# TODO : 507 Insufficient Storage
	# TODO : 508 Loop Detected
	NotExtendedError, # 510
	NetworkAuthenticationRequiredError, # 511
)

__all__ = (
	# Client Error
	'BadRequestError',  # 400
	'UnauthorizedError',  # 401
	'PaymentRequiredError',  # 402
	'ForbiddenError',  # 403
	'NotFoundError',  # 404
	'MethodNotAllowedError',  # 405
	'NotAcceptableError',  # 406
	'ProxyAuthenticationRequiredError',  # 407
	'RequestTimeoutError',  # 408
	'ConflictError',  # 409
	'GoneError',  # 410
	'LengthRequiredError',  # 411
	'PreconditionFailedError',  # 412
	'PayloadTooLargeError',  # 413
	'URITooLongError',  # 414
	'UnsupportedMediaTypeError',  # 415
	'RangeNotSatisfiableError',  # 416
	'ExpectationFailedError',  # 417
	# TODO : 418 I'm a teapot
	'UnprocessableEntityError',  # 422
	'TooEarlyError',  # 425
	'UpgradeRequiredError',  # 426
	'PreconditionRequiredError',  # 428
	'TooManyRequestsError',  # 429
	'RequestHeaderFieldsTooLargeError',  # 431
	# TODO : 451 Unavailable For Legal Reasons
	'LengthRequiredError',  # 411
	# Server Error
	'InternalServerError',  # 500
	'NotImplementedError',  # 501
	# TODO : 502 Bad Gateway
	'ServiceUnavailableError',  # 503
	# TODO : 504 Gateway Timeout
	'VersionNotSupportedError',  # 505
	# TODO : 506 Variant Also Negotiates
	# TODO : 507 Insufficient Storage
	# TODO : 508 Loop Detected
	'NotExtendedError',  # 510
	'NetworkAuthenticationRequiredError',  # 511
)
