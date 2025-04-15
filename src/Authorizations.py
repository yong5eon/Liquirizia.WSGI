# -*- coding: utf-8 -*-

from .Validators import (
	Authorization,
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
from enum import Enum

__all__ = (
	'HTTP',
	'Cookie',
	'Header',
	'Query',
	'OAuth2Type',
	'OAuth2',
)


class HTTP(Auth):
	def __init__(
		self,
		scheme: str,
		auth: Authorization,
		format: str = None,
		optional: bool = False,
		error: Error = None,
		errorParameters: Dict[str, str] = None,	
	):
		super().__init__(auth, optional, error)
		self.scheme = scheme
		self.format = format
		self.errorParameters = errorParameters
		return
	def __call__(self, request: Request):
		authorization: AuthorizationHeader = request.header('Authorization')
		if not authorization:
			if self.optional:
				return
			if self.error:
				raise self.error
			headers = None
			if self.errorParameters:
				headers = {
					'WWW-Authorization': '{} {}'.format(
						self.scheme,
						', '.join([
							'{}="{}"'.format(k, v) for k, v in self.errorParameters.items()
						]),
					),
				}
			raise UnauthorizedError('Authorization not found', headers=headers)
		if authorization.scheme != self.scheme:
			if self.schemeError:
				raise self.schemeError
			headers = None
			if self.errorParameters:
				headers = {
					'WWW-Authorization': '{} {}'.format(
						self.scheme,
						', '.join([
							'{}="{}"'.format(k, v) for k, v in self.errorParameters.items()
						]),
					),
				}
			raise UnauthorizedError('Authorization scheme not supported', headers=headers)
		session = self.auth(authorization.credentials)
		if not session:
			if self.optional:
				return
			if self.error:
				raise self.error
			headers = None
			if self.errorParameters:
				headers = {
					'WWW-Authorization': '{} {}'.format(
						self.scheme,
						', '.join([
							'{}="{}"'.format(k, v) for k, v in self.errorParameters.items()
						]),
					),
				}
			raise UnauthorizedError('Authorization failed', headers=headers)
		request.session = session
		return


class Cookie(Auth):
	def __init__(
		self,
		name: str,
		auth: Authorization,
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
		auth: Authorization,
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
		auth: Authorization,
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


class OAuth2Type(str, Enum):
	Password = 'password'
	Implicit = 'implicit'
	ClientCredentials = 'clientCredentials'
	AuthorizationCode = 'authorizationCode'
	def __str__(self): return self.value


class OAuth2(Auth):
	def __init__(
		self,
		type: OAuth2Type,
		scheme: str,
		auth: Authorization,
		optional: bool = False,
		error: Error = None,
		authorizationUrl: str = None,
		tokenUrl: str = None,
		refreshUrl: str = None,
		scope: Dict[str, str] = None,
	):
		super().__init__(auth, optional, error)
		self.type = type
		self.scheme = scheme
		self.kwargs = {}
		if authorizationUrl: self.kwargs['authorizationUrl'] = authorizationUrl
		if tokenUrl: self.kwargs['tokenUrl'] = tokenUrl
		if refreshUrl: self.kwargs['refreshUrl'] = refreshUrl
		if scope: self.kwargs['scope'] = scope
		return

	def __call__(self, request: Request) -> Any:
		authorization: AuthorizationHeader = request.header('Authorization')
		if not authorization:
			if self.optional:
				return
			if self.error:
				raise self.error
			kwargs = {
				'error': 'invalid_request',
				'error_description': 'Authorization not found',
			}
			kwargs.update(self.kwargs)
			raise UnauthorizedError('Authorization not found', headers={
				'WWW-Authorization': '{} {}'.format(
					self.scheme,
					', '.join([
						'{}="{}"'.format(k, v) for k, v in kwargs.items()
					]),
				),
			})
		if authorization.scheme != self.scheme:
			if self.optional:
				return
			if self.error:
				raise self.error
			kwargs = {
				'error': 'invalid_scheme',
				'error_description': 'Authorization scheme not supported',
			}
			kwargs.update(self.kwargs)
			headers = {
				'WWW-Authorization': '{} {}'.format(
					self.scheme,
					', '.join([
						'{}="{}"'.format(k, v) for k, v in kwargs.items()
					]),
				),
			}
			raise UnauthorizedError('Authorization scheme not supported', headers=headers)
		session = self.auth(authorization.credentials)
		if not session:
			if self.optional:
				return
			if self.error:
				raise self.error
			kwargs = {
				'error': 'invalid_token',
				'error_description': 'Authorization failed',
			}
			kwargs.update(self.kwargs)
			headers = {
				'WWW-Authorization': '{} {}'.format(
					self.scheme,
					', '.join([
						'{}="{}"'.format(k, v) for k, v in kwargs.items()
					]),
				),
			}
			raise UnauthorizedError('Authorization failed', headers=headers)
		request.session = session
		return
