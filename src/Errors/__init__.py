# -*- coding: utf-8 -*-

# client error
from .BadRequestError import BadRequestError  # 400
from .UnauthorizedError import UnauthorizedError  # 401
from .PaymentRequiredError import PaymentRequiredError  # 402
from .ForbiddenError import ForbiddenError  # 403
from .NotFoundError import NotFoundError  # 404
from .MethodNotAllowedError import MethodNotAllowedError  # 405
from .NotAcceptableError import NotAcceptableError  # 406
from .ProxyAuthenticationRequiredError import ProxyAuthenticationRequiredError  # 407
from .RequestTimeoutError import RequestTimeoutError  # 408
from .ConflictError import ConflictError  # 409
from .GoneError import GoneError  # 410
from .LengthRequiredError import LengthRequiredError  # 411
from .PreconditionFailedError import PreconditionFailedError
from .PayloadTooLargeError import PayloadTooLargeError  # 413
from .URITooLongError import URITooLongError  # 414
from .UnsupportedMediaTypeError import UnsupportedMediaTypeError  # 415
from .RangeNotSatisfiableError import RangeNotSatisfiableError  # 416
from .ExpectationFailedError import ExpectationFailedError  # 417
# TODO : 418 I'm a teapot
from .UnprocessableEntityError import UnprocessableEntityError  # 422
from .TooEarlyError import TooEarlyError  # 425
from .UpgradeRequiredError import UpgradeRequiredError  # 426
from .PreconditionRequiredError import PreconditionRequiredError  # 428
from .TooManyRequestsError import TooManyRequestsError  # 429
from .RequestHeaderFieldsTooLargeError import RequestHeaderFieldsTooLargeError  # 431
# TODO : 451 Unavailable For Legal Reasons

# server error
from .InternalServerError import InternalServerError  # 500
from .NotImplementedError import NotImplementedError  # 501
# TODO : 502 Bad Gateway
from .ServiceUnavailableError import ServiceUnavailableError  # 503
# TODO : 504 Gateway Timeout
from .VersionNotSupportedError import VersionNotSupportedError  # 505
# TODO : 506 Variant Also Negotiates
# TODO : 507 Insufficient Storage
# TODO : 508 Loop Detected
from .NotExtendedError import NotExtendedError  # 510
from .NetworkAuthenticationRequiredError import NetworkAuthenticationRequiredError  # 511

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
