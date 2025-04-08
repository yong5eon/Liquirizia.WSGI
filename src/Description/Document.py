# -*- coding: utf-8 -*-

from .Description import (
	Description,
	Response as ResponseDescription,
	Content as ContentDescription,
)

from Liquirizia.Description import Value, Schema

from uuid import uuid4
from collections.abc import MutableMapping
from typing import ItemsView, Iterator, KeysView, ValuesView, Any
from typing import Mapping, Optional, Sequence 

__all__ = (
	'Document',
	'Path',
	'Information',
	'Contact',
	'License',
	'Tag',
)


class Documentation(MutableMapping):
	def __init__(self, **kwargs):
		self.__document__ = kwargs
		return

	def __getitem__(self, key: Any) -> Any:
		return self.__document__.__getitem__(key)
	
	def __setitem__(self, key: Any, value: Any) -> None:
		return self.__document__.__setitem__(key, value)
	
	def __delitem__(self, key: Any) -> None:
		return self.__document__.__delitem__(key)
	
	def __iter__(self) -> Iterator:
		return self.__document__.__iter__()
	
	def __len__(self) -> int:
		return self.__document__.__len__()
	
	def __contains__(self, key: object) -> bool:
		return self.__document__.__contains__(key)
	
	def keys(self) -> KeysView:
		return self.__document__.keys()
	
	def items(self) -> ItemsView:
		return self.__document__.items()
	
	def values(self) -> ValuesView:
		return self.__document__.values()
	
	def __eq__(self, other: object) -> bool:
		return self.__document__.__eq__(other)
	
	def __ne__(self, value: object) -> bool:
		return self.__document__.__ne__(value)
	
	def get(self, key: object) -> Any:
		return self.__document__.get(key)


class ResponseHeader(Documentation):
	def __init__(self, header: Value):
		super().__init__(
			description=header['description'] if 'header' in header.keys() else None,
			schema={
				'type': str(header['type']) if 'type' in header.keys() else None,
				'format': header['format'] if 'format' in header.keys() else None,
				'minimum': header['min'] if 'min' in header.keys() else None,
				'maximum': header['max'] if 'max' in header.keys() else None,
				'default': header['default'] if 'default' in header.keys() else None,
				'enum': header['enum'] if 'enum' in header.keys() else None,
			},
			required=header['required'] if 'required' in header.keys() else None,
			deprecated=header['deprecated'] if 'deprecated' in header.keys() else None,
		)
		return
	
class Content(Documentation):
	def __init__(
		self,
		content: ContentDescription
	):
		super().__init__()
		if content.schema:
			if isinstance(content.schema, Schema):
				self['schema'] = content.schema.format
			else:
				self['schema'] = content.schema
		if content.example: self['example'] = content.example
		return


class Response(Documentation):
	def __init__(self, response: ResponseDescription):
		super().__init__(description=response.description)
		if response.content:
			response['content'] = {
				content.format: Content(content) for content in response.content
			}
		if response.headers:
			response['headers'] = {
				k: ResponseHeader(v) for k, v in response.headers.items()
			}
		return


class Path(Documentation):
	def __init__(
		self, 
		description: Description,
		id: str = None,
	):
		parameters = []
		for k, v in description.parameters.items() if description.parameters else []:
			_ = {
				'name': k,
				'in': 'path',
				'schema': {},
			}
			if 'description' in v.keys() and v['description']: _['description'] = v['description']
			if 'type' in v.keys() and v['type']: _['schema']['type'] = v['type']
			if 'format' in v.keys() and v['format']: _['schema']['format'] = v['format']
			if 'min' in v.keys() and v['min']: _['schema']['minimum'] = v['min']
			if 'max' in v.keys() and v['max']: _['schema']['maximum'] = v['max']
			if 'default' in v.keys() and v['default']: _['schema']['default'] = v['default']
			if 'enum' in v.keys() and v['enum']: _['schema']['enum'] = v['enum']
			_['required'] = v.required
			parameters.append(_)
		for k, v in description.qs.items() if description.qs else []:
			_ = {
				'name': k,
				'in': 'query',
				'schema': {},
			}
			if 'description' in v.keys() and v['description']: _['description'] = v['description']
			if 'type' in v.keys() and v['type']: _['schema']['type'] = v['type']
			if 'format' in v.keys() and v['format']: _['schema']['format'] = v['format']
			if 'min' in v.keys() and v['min']: _['schema']['minimum'] = v['min']
			if 'max' in v.keys() and v['max']: _['schema']['maximum'] = v['max']
			if 'default' in v.keys() and v['default']: _['schema']['default'] = v['default']
			if 'enum' in v.keys() and v['enum']: _['schema']['enum'] = v['enum']
			_['required'] = v.required
			parameters.append(_)
		for k, v in description.headers.items() if description.headers else []:
			_ = {
				'name': k,
				'in': 'header',
				'schema': {},
			}
			if 'description' in v.keys() and v['description']: _['description'] = v['description']
			if 'type' in v.keys() and v['type']: _['schema']['type'] = v['type']
			if 'format' in v.keys() and v['format']: _['schema']['format'] = v['format']
			if 'min' in v.keys() and v['min']: _['schema']['minimum'] = v['min']
			if 'max' in v.keys() and v['max']: _['schema']['maximum'] = v['max']
			if 'default' in v.keys() and v['default']: _['schema']['default'] = v['default']
			if 'enum' in v.keys() and v['enum']: _['schema']['enum'] = v['enum']
			_['required'] = v.required
			parameters.append(_)
		authenticates = []
		if description.auth:
			if description.auth.optional:
				authenticates.append({})
			authenticates.append({description.auth.name: []})
		responses = sorted(description.responses if description.responses else [], key=lambda x: x.status)
		super().__init__(operationId=id if id else uuid4().hex)
		if parameters: self['parameters'] = parameters
		if description.body:
			self['requestBody'] = {'required': description.body.required}
			if description.body.description:
				self['requestBody']['description'] = description.body.description
			if description.body.content:
				self['requestBody']['content'] = {
					content.format: Content(content) for content in description.body.content
				}
		if responses: 
			self['responses'] = {
				str(response.status): Response(response) for response in responses
			}
		if description.auth: self['security'] = authenticates
		if description.summary: self['summary'] = description.summary
		if description.description: self['description'] = description.description
		if description.tags: self['tags'] = description.tags
		return



class Contact(Documentation):
	def __init__(
		self,
		name: str = None,
		url: str = None,
		email: str = None,
	):
		super().__init__()
		if name: self.__document__['name'] = name
		if url: self.__document__['url'] = url
		if email: self.__document__['email'] = email
		return
	
class License(Documentation):
	def __init__(
		self,
		name: str,
		identifier: str = None,
		url: str = None,
	):
		super().__init__(
			name=name,
		)
		if identifier: self.__document__['identifier'] = identifier
		if url: self.__document__[url] = url
		return

class Information(Documentation):
	def __init__(
		self,
		title: str = '',
		version: str = '',
		summary: str = None,
		description: str = None,
		tos: str = None,
		contact: Contact = None,
		license: License = None,
	):
		super().__init__(
			title=title,
			version=version,
		)
		if summary: self.__document__['summary'] = summary
		if description: self.__document__['description'] = description
		if tos: self.__document__['termsOfService'] = tos
		if contact: self.__document__['contact'] = contact
		if license: self.__document__['license'] = license
		return


class Tag(Documentation):
	def __init__(
		self,
		name: str,
		description: str = None,
	):
		super().__init__(
			name=name,
		)
		if description: self.__document__['description'] = description
		return


class Document(Documentation):
	def __init__(
		self,
		info: Information,
		version='3.1.0',
		routes: Optional[Mapping[str, Mapping[str, Path]]] = None,
		schemas: Optional[Mapping[str, Mapping]] = None,
		authenticates: Optional[Mapping[str, Mapping]]= None,
		tags: Optional[Sequence[Tag]] = None,
	):
		self.__document__ = {
			'openapi': version,
			'info': info,
			'components': {
				'schemas': schemas if schemas else {},
				'securitySchemes': authenticates if authenticates else {},
			}
		}
		if routes:
			self.__document__['paths'] = routes
		if tags:
			self.__document__['tags'] = tags
		self.__document__['components']['schemas'] = schemas
		self.__document__['components']['securitySchemes'] = authenticates
		return


class Contact(Documentation):
	def __init__(
		self,
		name: str = None,
		url: str = None,
		email: str = None,
	):
		super().__init__()
		if name: self.__document__['name'] = name
		if url: self.__document__['url'] = url
		if email: self.__document__['email'] = email
		return
	
class License(Documentation):
	def __init__(
		self,
		name: str,
		identifier: str = None,
		url: str = None,
	):
		super().__init__(
			name=name,
		)
		if identifier: self.__document__['identifier'] = identifier
		if url: self.__document__[url] = url
		return

class Information(Documentation):
	def __init__(
		self,
		title: str = '',
		version: str = '',
		summary: str = None,
		description: str = None,
		tos: str = None,
		contact: Contact = None,
		license: License = None,
	):
		super().__init__(
			title=title,
			version=version,
		)
		if summary: self.__document__['summary'] = summary
		if description: self.__document__['description'] = description
		if tos: self.__document__['termsOfService'] = tos
		if contact: self.__document__['contact'] = contact
		if license: self.__document__['license'] = license
		return


class Tag(Documentation):
	def __init__(
		self,
		name: str,
		description: str = None,
	):
		super().__init__(
			name=name,
		)
		if description: self.__document__['description'] = description
		return
