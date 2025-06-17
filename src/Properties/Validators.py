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
from Liquirizia.WSGI.Errors.ClientError import UnauthorizedError
from ..Request import Request
from ..RequestReader import RequestReader
from ..Error import Error
from ..Errors import (
	ForbiddenError,
	BadRequestError,
)
from ..Description import Content
from .ContentReader import ContentReader

from abc import ABC, ABCMeta, abstractmethod
from typing import Dict, Sequence, Union, Any

__all__ = (
	'Origin',
	'Credentials',
	'Authorization',
	'Auth',
	'Parameters',
	'QueryString',
	'Headers',
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
		raise ForbiddenError(reason='Origin {} is not allowed'.format(origin))


class Credentials(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, request: Request) -> Any:
		raise NotImplementedError('{} must be implemented __call__'.format(
			self.__class__.__name__,
		))
	@property
	@abstractmethod
	def name(self) -> str:
		"""Return the name of the credentials"""
		raise NotImplementedError('{} must be implemented name'.format(
			self.__class__.__name__,
		))
	@property
	@abstractmethod
	def format(self) -> Dict[str, str]:
		"""Return the format of the credentials"""
		raise NotImplementedError('{} must be implemented format'.format(
			self.__class__.__name__,
		))


class Authorization(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, credentials: Any) -> Any:
		raise NotImplementedError('{} must be implemented __call__'.format(
			self.__class__.__name__,
		))


class Auth(object):
	def __init__(
		self,
		auth: Authorization,
		credentials: Credentials,
		optional: bool = False,
		error: Error = None,
	):
		self.auth = auth
		self.credentials = credentials
		self.optional = optional
		self.error = error
		return
	def __call__(self, request: Request):
		credentials = self.credentials(request)
		if not credentials:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError(reason='Credentials is not found')
		request.session = self.auth(credentials)
		return


class Parameters(object):
	"""Parameters Validator"""
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
				requiresError = BadRequestError(reason='Missing required query string {}'.format(
					', '.join(requires),
				))
			else:
				requiresError = BadRequestError(reason='Missing required query string')
		self.va = Validator(IsDataObject(
			IsRequiredInDataObject(*requires if requires else [], error=requiresError),
			IsMappingOfDataObject(qs),
		))
		self.format = format
		return
	def __call__(self, request: Request):
		request.args = self.va(request.args)
		return


class Headers(object):
	"""Headers Validator"""
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
				requiresError = BadRequestError(reason='Missing required headers {}'.format(
					','.join(requires),
				))
			else:
				requiresError = BadRequestError(reason='Missing required headers')
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
		content: Union[Content, Sequence[Content]] = None,
		required: bool = True,
	):
		self.reader = reader
		self.content = content
		if self.content:
			if not isinstance(self.content, (list, tuple)):
				self.content = [self.content]
		self.required = required
		return
	def __call__(self, request: Request, reader: RequestReader) -> Any:
		try:
			return self.reader(request, reader)
		except Error as e:
			raise e
		except Exception as e:
			raise BadRequestError(reason=str(e), error=e)
