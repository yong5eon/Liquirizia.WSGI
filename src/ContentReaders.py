# -*- coding: utf-8 -*-

from .ContentReader import ContentReader, TypeReader
from .RequestReader import RequestReader
from .Error import Error
from .Errors import BadRequestError

from urllib.parse import parse_qs, unquote_plus
from json import loads, JSONDecoder
from ast import literal_eval
from typing import Any

__all__ = (
	'ByteArrayContentReader',
	'TextContentReader',
	'TextEvaluateContentReader',
	'FormUrlEncodedContentReader',
	'JavaScriptObjectNotationContentReader',
)


class ByteArrayContentReader(ContentReader):
	def __init__(self, error: Error = None):
		self.error = error
		return
	def __call__(self, reader: RequestReader, size: int = -1) -> Any:
		try:
			return reader.read(size)
		except Exception as e:
			if self.error:
				raise self.error
			raise BadRequestError(str(e), error=e)


class TextContentReader(ContentReader):
	def __init__(self, charset: str ='utf-8', error: Error = None):
		self.charset = charset
		self.error = error
		return
	def __call__(self, reader: RequestReader, size: int = -1) -> Any:
		try:
			return reader.read(size).decode(self.charset)
		except Exception as e:
			if self.error:
				raise self.error
			raise BadRequestError(str(e), error=e)


class TextEvaluateContentReader(ContentReader):
	def __init__(self, charset: str ='utf-8', error: Error = None):
		self.charset = charset
		self.error = error
		return
	def __call__(self, reader: RequestReader, size: int = -1) -> Any:
		try:
			return eval(reader.read(size).decode(self.charset))
		except Exception as e:
			if self.error:
				raise self.error
			raise BadRequestError(str(e), error=e)


class FormUrlEncodedContentReader(ContentReader):
	def __init__(self, charset: str = 'utf-8', error: Error = None):
		self.charset = charset
		self.error = error
		return
	def __call__(self, reader: RequestReader, size: int = -1) -> Any:
		try:
			content = reader.read(size).decode(self.charset)
			qs = parse_qs(content, keep_blank_values=True)
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
			if self.error:
				raise self.error
			raise BadRequestError(str(e), error=e)


class JavaScriptObjectNotationTypeDecoder(JSONDecoder):
	def __init__(self, typereader: TypeReader = None):
		self.typereader = typereader
		return
	def __call__(self, o: Any) -> Any:
		if isinstance(o, dict):
			for k, v in o.items():
				if isinstance(v, (dict, list)):
					o[k] = self.decode(v)
					continue
				o[k] = self.typereader(v) if self.typereader else v
			return o
		if isinstance(o, list):
			for i in range(len(o)):
				if isinstance(o[i], (dict, list)):
					o[i] = self.decode(o[i])
					continue
				o[i] = self.typereader(o[i]) if self.typereader else o[i]
			return o
		return self.typereader(o) if self.typereader else o


class JavaScriptObjectNotationContentReader(ContentReader):
	def __init__(self, typereader: TypeReader = None, charset: str = 'utf-8', error: Error = None):
		self.typereader = typereader
		self.charset = charset
		self.error = error
		return
	def __call__(self, reader: RequestReader, size: int = -1) -> Any:
		try:
			content = reader.read(size)
			return loads(content.decode(self.charset), object_hook=JavaScriptObjectNotationTypeDecoder(typereader=self.typereader))
		except Exception as e:
			if self.error:
				raise self.error
			raise BadRequestError(str(e), error=e)
