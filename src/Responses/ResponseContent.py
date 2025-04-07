# -*- coding: utf-8 -*-

from ..Response import Response
from ..Encoders import *

from typing import Dict, Any, Mapping

__all__ = (
	'ResponseText'
	'ResponseHTML'
	'ResponseJSON'
)

class ResponseText(Response):
	"""Response HTML Class"""
	def __init__(self, body: str, status=200, message='OK', headers: Dict[str, Any] = {}):
		encode = TextEncoder('utf-8')
		super(ResponseHTML, self).__init__(
			status=status,
			message=message,
			headers=headers,
			body=encode(body),
			format='text/plain',
			charset='utf-8',
		)
		return

class ResponseHTML(Response):
	"""Response HTML Class"""
	def __init__(self, body: str, status=200, message='OK', headers: Dict[str, Any] = {}):
		encode = TextEncoder('utf-8')
		super(ResponseHTML, self).__init__(
			status=status,
			message=message,
			headers=headers,
			body=encode(body),
			format='text/html',
			charset='utf-8',
		)
		return


class ResponseJSON(Response):
	"""Response JSON Class"""
	def __init__(self, body: Mapping, status=200, message='OK', headers: Dict[str, Any ]= {}):
		encode = JavaScriptObjectNotationEncoder('utf-8')
		super().__init__(
			status=status,
			message=message,
			headers=headers,
			body=encode(body),
			format='application/json',
			charset='utf-8',
		)
		return
