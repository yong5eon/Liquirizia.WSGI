# -*- coding: utf-8 -*-

from ..Response import Response
from ..Encoders import *
from ..Content import Content
from ..Encoder import TypeEncoder

from typing import Dict, Any

__all__ = (
	'ResponseText'
	'ResponseHTML'
	'ResponseJSON'
	'ResponseContent',
)

class ResponseText(Response):
	"""Response HTML Class"""
	def __init__(self, text: str, status=200, message='OK', headers: Dict[str, Any] = {}):
		encode = TextEncoder('utf-8')
		super(ResponseText, self).__init__(
			status=status,
			message=message,
			headers=headers,
			body=encode(text),
			format='text/plain',
			charset='utf-8',
		)
		return

class ResponseHTML(Response):
	"""Response HTML Class"""
	def __init__(self, html: str, status=200, message='OK', headers: Dict[str, Any] = {}):
		encode = TextEncoder('utf-8')
		super(ResponseHTML, self).__init__(
			status=status,
			message=message,
			headers=headers,
			body=encode(html),
			format='text/html',
			charset='utf-8',
		)
		return


class ResponseJSON(Response):
	"""Response JSON Class"""
	def __init__(
			self,
			o: Any,
			typeenc: TypeEncoder = JavaScriptObjectNotationTypeEncoder(),
			charset: str = 'utf-8',
			status=200,
			message='OK',
			headers: Dict[str, Any ]= {},
		):
		encode = JavaScriptObjectNotationEncoder(charset=charset, typeenc=typeenc)
		super().__init__(
			status=status,
			message=message,
			headers=headers,
			body=encode(o),
			format='application/json',
			charset=charset,
		)
		return


class ResponseContent(Response):
	"""Response Content Class"""
	def __init__(self, content: Content, status=200, message='OK', headers: Dict[str, Any] = {}):
		_ = content.headers()
		_.update(headers)
		super().__init__(
			status=status,
			message=message,
			headers=_,
			body=content.body,
			format=content.format,
			charset=content.charset,
		)
		return
