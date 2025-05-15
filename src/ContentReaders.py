# -*- coding: utf-8 -*-

from .ContentReader import ContentReader, TypeReader
from .Request import Request
from .RequestReader import RequestReader
from .Error import Error
from .Errors import BadRequestError, UnsupportedMediaTypeError
from .Headers import ContentType

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
	def __call__(self, request: Request, reader: RequestReader) -> Any:
		try:
			return reader.read(request.size)
		except Exception as e:
			if self.error:
				raise self.error
			raise BadRequestError(reason=str(e), error=e)


class TextContentReader(ContentReader):
	def __init__(
		self,
		error: Error = None,
		typeerror: Error = None,
	):
		self.error = error
		self.typeerror = typeerror
		return
	def __call__(self, request: Request, reader: RequestReader) -> Any:
		try:
			type: ContentType = request.header('Content-Type')
			if not type:
				if self.error: raise self.error
				raise BadRequestError(reason='Missing Content-Type header')
			if not type.format.lower().startswith('text/'):
				if self.typeerror: raise self.typeerror
				raise UnsupportedMediaTypeError(reason='Invalid Content-Type header')
			return reader.read(request.size).decode(type.charset if type.charset else '')
		except Exception as e:
			if self.error:
				raise self.error
			raise BadRequestError(reason=str(e), error=e)


class TextEvaluateContentReader(ContentReader):
	def __init__(
		self,
		error: Error = None,
		typeerror: Error = None,
	):
		self.error = error
		self.typeerror = typeerror
		return
	def __call__(self, request: Request, reader: RequestReader) -> Any:
		try:
			type: ContentType = request.header('Content-Type')
			if not type:
				if self.error: raise self.error
				raise BadRequestError(reason='Missing Content-Type header')
			if not type.format.lower().startswith('text/'):
				if self.typeerror: raise self.typeerror
				raise UnsupportedMediaTypeError(reason='Invalid Content-Type header')
			return eval(reader.read(request.size).decode(type.charset if type.charset else ''))
		except Exception as e:
			if self.error:
				raise self.error
			raise BadRequestError(reason=str(e), error=e)


class FormUrlEncodedContentReader(ContentReader):
	def __init__(self, error: Error = None, typeerror: Error = None):
		self.error = error
		self.typeerror = typeerror
		return
	def __call__(self, request: Request, reader: RequestReader) -> Any:
		try:
			type: ContentType = request.header('Content-Type')
			if not type:
				if self.error: raise self.error
				raise BadRequestError(reason='Missing Content-Type header')
			if type.format.lower() != 'application/x-www-form-urlencoded':
				if self.typeerror: raise self.typeerror
				raise UnsupportedMediaTypeError(reason='Invalid Content-Type header')
			content = reader.read(request.size).decode(type.charset if type.charset else '')
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
			raise BadRequestError(reason=str(e), error=e)


class JavaScriptObjectNotationTypeDecoder:
	def __init__(self, typereader: TypeReader = None):
		self.typereader = typereader
		return
	def __call__(self, o: Any) -> Any:
		if isinstance(o, dict):
			for k, v in o.items():
				if isinstance(v, (dict, list)):
					o[k] = self.__call__(v)
					continue
				o[k] = self.typereader(v) if self.typereader else v
			return o
		if isinstance(o, list):
			for i in range(len(o)):
				if isinstance(o[i], (dict, list)):
					o[i] = self.__call__(o[i])
					continue
				o[i] = self.typereader(o[i]) if self.typereader else o[i]
			return o
		return self.typereader(o) if self.typereader else o


class JavaScriptObjectNotationContentReader(ContentReader):
	def __init__(self, typereader: TypeReader = None, error: Error = None, typeerror: Error = None):
		self.typereader = typereader
		self.error = error
		self.typeerror = typeerror
		return
	def __call__(self, request: Request, reader: RequestReader) -> Any:
		try:
			type: ContentType = request.header('Content-Type')
			if not type:
				if self.error: raise self.error
				raise BadRequestError(reason='Missing Content-Type header')
			if type.format.lower() != 'application/json':
				if self.typeerror: raise self.typeerror
				raise UnsupportedMediaTypeError(reason='Invalid Content-Type header')
			content = reader.read(request.size)
			return loads(content.decode(type.charset if type.charset else ''), object_hook=JavaScriptObjectNotationTypeDecoder(typereader=self.typereader))
		except Exception as e:
			if self.error:
				raise self.error
			raise BadRequestError(reason=str(e), error=e)
