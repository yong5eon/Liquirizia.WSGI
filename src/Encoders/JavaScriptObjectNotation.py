# -*- coding: utf-8 -*-

from ..Encoder import Encoder, TypeEncoder


from collections.abc import MutableSequence, Sequence, Mapping, Set
from datetime import datetime, date, time
from decimal import Decimal
from json import dumps
from dataclasses import is_dataclass, asdict

__all__ = (
	'JavaScriptObjectNotationTypeEncoder',
	'JavaScriptObjectNotationEncoder',
)


class JavaScriptObjectNotationTypeEncoder(TypeEncoder):
	"""Type Encoder for JavaScriptObjectNotation"""

	def __call__(self, obj):
		if isinstance(obj, Decimal):
			return float(obj)
		if isinstance(obj, MutableSequence):
			return list(obj)
		if isinstance(obj, Sequence):
			return tuple(obj)
		if isinstance(obj, Set):
			return tuple(obj)
		if isinstance(obj, Mapping):
			return dict(obj)
		if isinstance(obj, (datetime, date, time)):
			return obj.isoformat()
		if is_dataclass(obj):
			return asdict(obj)
		raise RuntimeError('{} {} is not a supported type in {}'.format(type(obj), obj, self.__class__.__name__))


class JavaScriptObjectNotationEncoder(Encoder):
	"""Encoder Class for JSON"""
	def __init__(self, charset: str = 'utf-8', typeenc: TypeEncoder = JavaScriptObjectNotationTypeEncoder(), ensure_ascii: bool = False):
		self.charset = charset
		self.typeencoder = typeenc
		self.ea = ensure_ascii
		return
	def __call__(self, obj):
		return dumps(
			obj, 
			default=self.typeencoder,
			ensure_ascii=self.ea, 
		).encode(self.charset)
