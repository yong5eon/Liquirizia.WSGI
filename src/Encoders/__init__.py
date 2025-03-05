# -*- coding: utf-8 -*-

from ..Encoder import Encoder

from .JavaScriptObjectNotation import JavaScriptObjectNotationEncoder

from typing import Any

__all__ = (
	'TextEncoder',
	'JavaScriptObjectNotationEncoder',
)


class TextEncoder(Encoder):
	def __init__(self, charset: str ='utf-8'):
		self.chs = charset
		return
	def __call__(self, body: Any) -> bytes:
		return str(body).encode(self.charset)
	@property
	def format(self): return 'text/plain'
	@property
	def charset(self): return self.chs

