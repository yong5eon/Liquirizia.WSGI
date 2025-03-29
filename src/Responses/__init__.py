# -*- coding: utf-8 -*-

# Error
from .ResponseError import ResponseError
# Content
from .ResponseContent import (
	ResponseHTML,
	ResponseJSON,
)
# File
from .ResponseFile import ResponseFile
# Buffer
from .ResponseBuffer import ResponseBuffer
# 1XX Informational
# 2XX Succesful
from .ResponseSuccesful import (
	ResponseOK, # 200
	ResponseCreated, # 201
	ResponseAccepted, # 202
	ResponseNoContent, # 204
)
# 3XX Redirection
from .ResponseRedirection import (
	ResponseMovePermanently, # 301
	ResponseFound, # 302
	ResponseNotModified  # 304
)
# 4XX Client Error
from .ResponseClientError import (
	ResponseBadRequest, # 400 Bad Request
	ResponseUnauthorized, # 401 Unauthorized
	ResponsePaymentRequired, # 402 Payment Required
	ResponseForbidden, # 403 Forbidden
	ResponseNotFound, # 404 Not Found
	ResponseMethodNotAllowed, # 405 Method Not Allowed
	ResponseNotAcceptable, # 406 Not Acceptable
	ResponseProxyAuthenticationRequired, # 407 Proxy Authentication Required
	ResponseRequestTimeout, # 408 Request Timeout
	ResponseConflict, # 409 Conflict
	ResponseGone, # 410 Gone
	ResponseLengthRequired, # 411 Length Required
	ResponsePreconditionFailed, # 412 Precondition Failed
	ResponsePayloadTooLarge, # 413 Payload Too Large
	ResponseURITooLong, # 414 URI Too Long
	ResponseUnsupportedMediaType, # 415 Unsupported Media Type
	ResponseRangeNotSatisfiable, # 416 Range Not Satisfiable
	ResponseExpectationFailed, # 417 Expectation Failed
	# TODO : 418 I'm a teapot
	ResponseMisdirectedRequest, # 421 Misdirected Request
	ResponseUnprocessableEntity, # 422 Unprocessable Entity
	ResponseLocked, # 423 Locked
	ResponseFailedDependency, # 424 Failed Dependency
	ResponseTooEarly, # 425 Too Early
	ResponseUpgradeRequired, # 426 Upgrade Required
	ResponseUnassigned, # 427 Unassigned
	ResponsePreconditionRequired, # 428 Precondition Required
	ResponseTooManyRequests, # 429 Too Many Requests
	ResponseRequestHeaderFieldsTooLarge, # 431 Request Header Fields Too Large
	ResponseUnavailableForLegalReasons, # 451 Unavailable For Legal Reasons
)
# 5XX Server Error
from .ResponseServerError import (
	ResponseInternalServerError,
	ResponseNotImplemented,
	ResponseServiceUnavailable,
)

__all__ = (
	'ResponseError',  # Response Error
	'ResponseHTML',  # Response HTML
	'ResponseJSON',  # Response JSON
	'ResponseFile',  # Response File
	'ResponseBuffer',  # Response Buffer(Bytes)
	# 1XX Informational
	# 2XX Succesful
	'ResponseOK', # 200
	'ResponseCreated', # 201
	'ResponseAccepted',  # 202
	'ResponseNoContent',  # 204
	# 3XX Redirection
	'ResponseMovePermanently', # 301
	'ResponseFound',  # 302
	'ResponseNotModified', # 304
	# 4XX Client Error
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
	# 5XX Server Error
	'ResponseInternalServerError',
	'ResponseNotImplemented',
	'ResponseServiceUnavailable',
)
