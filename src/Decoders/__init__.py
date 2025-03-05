# -*- coding: utf-8 -*-

from ..Decoder import Decoder
from ..Errors import BadRequestError

from urllib.parse import parse_qs, unquote_plus
from json import loads, JSONDecoder
from ast import literal_eval
from typing import Any

__all__ = (
	'TextDecoder',
	'FormUrlEncodedDecoder',
	'JavaScriptObjectNotataionDecoder',
)


class TextDecoder(Decoder):
	def __init__(self, charset: str ='utf-8'):
		self.chs = charset
		return
	def __call__(self, body: bytes) -> Any:
		try:
			return body.decode(self.charset)
		except Exception as e:
			raise BadRequestError(str(e), error=e)
	@property
	def format(self): return 'text/plain'
	@property
	def charset(self): return self.chs


class FormUrlEncodedDecoder(Decoder):
	def __init__(self, charset: str = 'utf-8'):
		self.chs = charset
		return
	def __call__(self, body: bytes) -> Any:
		try:
			body = body.decode(self.charset)
			qs = parse_qs(body, keep_blank_values=True)
			q = {}
			for (key, value) in qs.items():
				if len(value) == 0:
					q[key] = None
					continue
				elif len(value) == 1:
					try:
						q[key] = unquote_plus(literal_eval(value[0]))
					except:
						q[key] = unquote_plus(value[0]) if len(value[0]) else None
					continue
				else:
					q[key] = unquote_plus(value)
			return q
		except Exception as e:
			raise BadRequestError(str(e), error=e)
	@property
	def format(self): return 'application/x-www-form-urlencoded'
	@property
	def charset(self): return self.chs


class JavaScriptObjectNotationDecoder(Decoder):
	def __init__(self, charset: str = 'utf-8'):
		self.chs = charset
		return
	def __call__(self, body: bytes) -> Any:
		try:
			return loads(body, cls=JSONDecoder)
		except Exception as e:
			raise BadRequestError(str(e), error=e)
	@property
	def format(self): return 'application/json'
	@property
	def charset(self): return self.chs
