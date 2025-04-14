# -*- coding: utf-8 -*-

from typing import Any, Iterator, KeysView, ItemsView, ValuesView, Mapping
from typing import Dict, Union

__all__ = (
	'Authenticate',
	'OAuth2',
	'HTTP',
	'Header',
	'Query',
	'Cookie',
	'TLS',
	'OpenIdConnect',
)

class Authenticate(Mapping):
	def __init__(self, **kwargs):
		self.__properties__ = kwargs
		return

	def __getitem__(self, key: Any) -> Any:
		return self.__properties__.__getitem__(key)
	
	def __setitem__(self, key: Any, value: Any) -> None:
		return self.__properties__.__setitem__(key, value)
	
	def __delitem__(self, key: Any) -> None:
		return self.__properties__.__delitem__(key)
	
	def __iter__(self) -> Iterator:
		return self.__properties__.__iter__()
	
	def __len__(self) -> int:
		return self.__properties__.__len__()
	
	def __contains__(self, key: object) -> bool:
		return self.__properties__.__contains__(key)
	
	def keys(self) -> KeysView:
		return self.__properties__.keys()
	
	def items(self) -> ItemsView:
		return self.__properties__.items()
	
	def values(self) -> ValuesView:
		return self.__properties__.values()
	
	def __eq__(self, other: object) -> bool:
		return self.__properties__.__eq__(other)
	
	def __ne__(self, value: object) -> bool:
		return self.__properties__.__ne__(value)
	
	def get(self, key: object) -> Any:
		return self.__properties__.get(key)


class OAuth2(Authenticate):
	def __init__(
		self,
		type: str,
		authorizationUrl: str = None,
		tokenUrl: str = None,
		refreshUrl: str = None,
		scopes: Dict[str, str] = None,
		description: str = None,
	):
		super().__init__(
			type='oauth2',
			flows={
				type: {}
			},
		)
		if authorizationUrl: self['flows'][type]['authorizationUrl'] = authorizationUrl
		if tokenUrl: self['flows'][type]['tokenUrl'] = tokenUrl
		if refreshUrl: self['flows'][type]['refreshUrl'] = refreshUrl
		if scopes: self['flows'][type]['scopes'] = scopes
		if description: self['description'] = description
		return

	
class HTTP(Authenticate):
	def __init__(
		self,
		format: str,
		bearerFormat: str = 'bearer',
		description: str = None,
	):
		super().__init__(
			type='http',
			scheme=format,
			bearerFormat=bearerFormat,
		)
		if description: self['description'] = description
		return


class Header(Authenticate):
	def __init__(
		self,
		name: str,
		description: str = None,
	):
		super().__init__(
			type='apiKey',
			name=name,
		)
		if description: self['description'] = description
		self['in'] = 'header'
		return

class Query(Authenticate):
	def __init__(
		self,
		name: str,
		description: str = None,
	):
		super().__init__(
			type='apiKey',
			name=name,
		)
		if description: self['description'] = description
		self['in'] = 'query'
		return


class Cookie(Authenticate):
	def __init__(
		self,
		name: str,
		description: str = None,
	):
		super().__init__(
			type='apiKey',
			name=name,
		)
		if description: self['description'] = description
		self['in'] = 'cookie'
		return


class TLS(Authenticate):
	def __init__(
		self,
		description: str = None,
	):
		super().__init__(
			type='mutualTLS',
		)
		if description: self['description'] = description
		return


class OpenIdConnect(Authenticate):
	def __init__(
		self,
		url: str,
		description: str = None,
	):
		super().__init__(
			type='openIdConnect',
			openIdConnectUrl=url,
		)
		if description: self['description'] = description
		return
	
