# -*- coding: utf-8 -*-

from .Validators import (
	Authenticate,
	Auth,
)

from .Request import Request
from .Error import Error
from .Errors import  UnauthorizedError
from .Headers import (
	Authorization as AuthorizationHeader,
	Cookie,
)

from typing import Dict, Any

__all__ = (
	'HTTP',
	'Cookie',
	'Header',
	'Query',
)


class HTTP(Auth):
	def __init__(
		self,
		scheme: str,
		auth: Authenticate,
		format: str = None,
		optional: bool = False,
		schemeError: Error = None,
		schemeErrorParameters: Dict[str, Any] = None,
		error: Error = None,
	):
		super().__init__(auth, optional, error)
		self.scheme = scheme
		self.format = format
		self.schemeError = schemeError
		self.schemeErrorParameters = schemeErrorParameters
		return
	def __call__(self, request: Request):
		authorization: AuthorizationHeader = request.header('Authorization')
		if not authorization:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Authorization not found')
		if authorization.scheme != self.scheme:
			if self.schemeError:
				raise self.schemeError
			headers = None
			if self.schemeErrorParameters:
				headers = {
					'WWW-Authenticate': '{} {}'.format(
						self.scheme,
						','.join([
							'{}="{}"'.format(k, v) for k, v in self.schemeErrorParameters.items()
						]),
					),
				}
			raise UnauthorizedError(
				'Authorization scheme not supported',
				headers=headers,
			)
		session = self.auth(authorization.credentials)
		if not session:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Authorization failed')
		request.session = session
		return


class Cookie(Auth):
	def __init__(
		self,
		name: str,
		auth: Authenticate,
		optional: bool = False,
		error: Error = None,
	):
		super().__init__(auth, optional, error)
		self.name = name
		return
	def __call__(self, request: Request) -> Any:
		cookies = request.header('Cookie')
		if not cookies:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Cookie is not found')
		_ = None
		for cookie in cookies:
			if cookie.name == self.name:
				_ = cookie
				break
		if not _:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Cookie {} is not found'.format(self.name))
		session = self.auth(_)
		if not session:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Cookie {} is not valid'.format(self.name))
		request.session = session
		return


class Header(Auth):
	def __init__(
		self,
		name: str,
		auth: Authenticate,
		optional: bool = False,
		error: Error = None,
	):
		super().__init__(auth, optional, error)
		self.name = name
		return
	def __call__(self, request: Request) -> Any:
		_ = request.header(self.name)
		if not _:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Header {} is not found'.format(self.name))
		session = self.auth(_)
		if not session:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Cookie {} is not valid'.format(self.name))
		request.session = session
		return


class Query(Auth):
	def __init__(
		self,
		name: str,
		auth: Authenticate,
		optional: bool = False,
		error: Error = None,
	):
		super().__init__(auth, optional, error)
		self.name = name
		return
	def __call__(self, request: Request) -> Any:
		if not hasattr(request.qs, self.name):
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Query {} is not found'.format(self.name))
		session = self.auth(getattr(request.qs, self.name))
		if not session:
			if self.optional:
				return
			if self.error:
				raise self.error
			raise UnauthorizedError('Query {} is not valid'.format(self.name))
		request.session = session
		return

