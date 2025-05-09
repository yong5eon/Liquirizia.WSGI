# -*- coding: utf-8 -*-

from Liquirizia.Validator import Validator, Pattern
from Liquirizia.Validator.Patterns import IsDataObject, IsObject
from Liquirizia.Validator.Patterns.DataObject import (
	IsRequiredIn as IsRequiredInDataObject,
	IsMappingOf as IsMappingOfDataObject,
)
from Liquirizia.Validator.Patterns.Object import (
	IsRequiredIn as IsRequiredInObject,
	IsMappingOf as IsMappingOfObject,
)
from Liquirizia.Description import (
	Value,
	Schema,
)
from .Request import Request
from .RequestReader import RequestReader
from .ContentReader import ContentReader
from .Error import Error
from .Errors import (
	UnauthorizedError,
	ForbiddenError,
	BadRequestError,
	UnsupportedMediaTypeError,
)
from .Headers import (
	ContentType,
)

from abc import ABC, ABCMeta, abstractmethod
from typing import Dict, Sequence, Union, Any

__all__ = (
	'Origin',
	'Authorization',
	'Auth',
	'Parameter',
	'QueryString',
	'Header',
	'Body',
)


class Origin(object):
	def __init__(
		self,
		origin: Union[str, Sequence[str]] = None,
		all: bool = False,
		error: Error = None,
	):
		self.matches = origin
		if not isinstance(self.matches, (list, tuple)):
			self.matches = [self.matches]
		self.all = all 
		self.error = error
		return
	def __call__(self, request: Request):
		origin = request.header('Origin')
		match = None
		for m in self.matches:
			if origin == m:
				match = m
				break
		if match or self.all:
			return
		if self.error:
			raise self.error
		raise ForbiddenError('Origin {} is not allowed'.format(origin))


class Authorization(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, value: Any) -> Any:
		raise NotImplementedError('{} must be implemented __call__'.format(
			self.__class__.__name__,
		))


class Auth(ABC):
	def __init__(
		self,
		auth: Authorization,
		optional: bool = False,
		error: Error = None,
	):
		self.auth = auth
		self.optional = optional
		self.error = error
		return
	@abstractmethod
	def __call__(self, request: Request):
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))


class Parameter(object):
	"""Paramter Validator"""
	def __init__(
		self,
		parameters : Dict[str, Union[Pattern, Sequence[Pattern]]],
		format: Dict[str, Union[Value, Schema]] = None,
	):
		self.va = Validator(IsDataObject(IsMappingOfDataObject(parameters)))
		self.format = format
		return
	def __call__(self, request: Request):
		request.params = self.va(request.params)
		return


class QueryString(object):
	"""QueryString Validator"""
	def __init__(
		self,
		qs: Dict[str, Union[Pattern, Sequence[Pattern]]],
		requires: Union[str, Sequence[str]] = None,
		requiresError: Error = None,
		format: Dict[str, Union[Value, Schema]] = None,
	):
		if not requiresError:
			if requires:
				if not isinstance(requires, (list, tuple)):
					requires = [requires]
				requiresError = BadRequestError('Missing required query string {}'.format(
					','.join(requires),
				))
			else:
				requiresError = BadRequestError('Missing required query string')
		self.va = Validator(IsDataObject(
			IsRequiredInDataObject(*requires if requires else [], error=requiresError),
			IsMappingOfDataObject(qs),
		))
		self.format = format
		return
	def __call__(self, request: Request):
		request.args = self.va(request.args)
		return


class Header(object):
	"""Header Validator"""
	def __init__(
		self,
		headers: Dict[str, Union[Pattern, Sequence[Pattern]]],
		requires: Union[str, Sequence[str]] = None,
		requiresError: Error = None,
		format: Dict[str, Union[Value, Schema]] = None,
	):
		if not requiresError:
			if requires:
				if not isinstance(requires, (list, tuple)):
					requires = [requires]
				requiresError = BadRequestError('Missing required headers {}'.format(
					','.join(requires),
				))
			else:
				requiresError = BadRequestError('Missing required headers')
		self.va = Validator(IsObject(
			IsRequiredInObject(*requires if requires else [], error=requiresError),
			IsMappingOfObject(headers),
		))
		self.headers = headers.keys()
		self.format = format 
		return
	def __call__(self, request: Request):
		headers = {}
		for k, v in request.headers():
			headers[k] = v
		headers = self.va(headers)
		for k, v in headers.items():
			request.header(k, v)
		return


class Body(object):
	"""Body Validator"""
	def __init__(
		self,
		reader: ContentReader,
		content: Pattern = None,
		type: str = None,
		format: Union[Value, Schema] = None,
		example: Any = None,
		required: bool = True,
	):
		self.reader = reader
		self.va = Validator(content) if content else Validator()
		self.type = type
		self.format = format
		self.example = example
		self.required = required
		return
	def __call__(self, request: Request, reader: RequestReader) -> Any:
		try:
			return self.va(self.reader(request, reader))
		except Error as e:
			raise e
		except Exception as e:
			raise BadRequestError(str(e), error=e)
