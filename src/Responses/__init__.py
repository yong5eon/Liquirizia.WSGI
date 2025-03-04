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
	ResponseBadRequest, # 400
	ResponseNotFound,  # 404
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
	'ResponseBadRequest', # 400
	'ResponseNotFound',  # 404
	# 5XX Server Error
	'ResponseInternalServerError',
	'ResponseNotImplemented',
	'ResponseServiceUnavailable',
)
