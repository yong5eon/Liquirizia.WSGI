# -*- coding: utf-8 -*-

from ..Encoder import Encoder

from .JavaScriptObjectNotation import (
	JavaScriptObjectNotationEncoder,
	JavaScriptObjectNotationTypeEncoder,
)

from typing import Any

__all__ = (
	'TextEncoder',
	'JavaScriptObjectNotationEncoder',
	'JavaScriptObjectNotationTypeEncoder',
)


class TextEncoder(Encoder):
	def __init__(self, charset: str ='utf-8'):
		self.charset = charset
		return
	def __call__(self, body: Any) -> bytes:
		return str(body).encode(self.charset)

