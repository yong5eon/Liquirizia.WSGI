# -*- coding: utf-8 -*-

from ..Response import Response

from typing import Dict, Any

__all__ = (
	'ResponseOK', # 200
	'ResponseCreated', # 201
	'ResponseAccepted', # 202
	# TODO : 203 Non-Authoritative Information
	'ResponseNoContent', # 204
	# TODO : 205 Reset Content
	# TODO : 206 Partial Content
	
)


class ResponseOK(Response):
	"""Response 200 OK Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super().__init__(
			status=200,
			message='OK',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseCreated(Response):
	"""Response 201 Created Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super().__init__(
			status=201,
			message='Created',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseAccepted(Response):
	"""Response 202 Accepted Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super().__init__(
			status=202,
			message='Accepted',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return


class ResponseNoContent(Response):
	"""Response 204 No Content Class"""
	def __init__(self, body=None, format=None, charset=None, headers: Dict[str, Any] = {}):
		super().__init__(
			status=204,
			message='No Content',
			headers=headers,
			body=body,
			format=format,
			charset=charset,
		)
		return
