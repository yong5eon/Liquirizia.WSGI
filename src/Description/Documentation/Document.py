# -*- coding: utf-8 -*-

from .Documentation import Documentation

from .Information import (
	Information,
	Tag,
)

from ..Description import (
	Description,
	Response as ResponseDescription,
	Content as ContentDescription,
	Schema,
)

from Liquirizia.Description import Value

from uuid import uuid4

from typing import Mapping, Optional, Sequence 

__all__ = (
	'Document',
	'Path',
)


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
	
class ResponseContent(Documentation):
	def __init__(
		self,
		content: ContentDescription
	):
		super().__init__(
			schema={'$ref': '#/components/schemas/{}'.format(content.schema.name)} if isinstance(content.schema, Schema) else content.schema,
		)
		if content.example: self['example'] = content.example
		return


class Response(Documentation):
	def __init__(self, response: ResponseDescription):
		super().__init__(
			description=response.description,
			content={
				content.format: ResponseContent(content) for content in response.content
			} if response.content else {},
			headers={
				k: ResponseHeader(v) for k, v in response.headers.items()
			} if response.headers else {},
		)
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
			if 'description' in v.keys(): _['description'] = v['description']
			if 'type' in v.keys(): _['schema']['type'] = v['type']
			if 'format' in v.keys(): _['schema']['format'] = v['format']
			if 'min' in v.keys(): _['schema']['minimum'] = v['min']
			if 'max' in v.keys(): _['schema']['maximum'] = v['max']
			if 'default' in v.keys(): _['schema']['default'] = v['default']
			if 'enum' in v.keys(): _['schema']['enum'] = v['enum']
			if 'required' in v.keys(): _['required'] = v['required']
			parameters.append(_)
		for k, v in description.qs.items() if description.qs else []:
			_ = {
				'name': k,
				'in': 'query',
				'schema': {},
			}
			if 'description' in v.keys(): _['description'] = v['description']
			if 'type' in v.keys(): _['schema']['type'] = v['type']
			if 'format' in v.keys(): _['schema']['format'] = v['format']
			if 'min' in v.keys(): _['schema']['minimum'] = v['min']
			if 'max' in v.keys(): _['schema']['maximum'] = v['max']
			if 'default' in v.keys(): _['schema']['default'] = v['default']
			if 'enum' in v.keys(): _['schema']['enum'] = v['enum']
			if 'required' in v.keys(): _['required'] = v['required']
			parameters.append(_)
		for k, v in description.headers.items() if description.headers else []:
			_ = {
				'name': k,
				'in': 'header',
				'schema': {},
			}
			if 'description' in v.keys(): _['description'] = v['description']
			if 'type' in v.keys(): _['schema']['type'] = v['type']
			if 'format' in v.keys(): _['schema']['format'] = v['format']
			if 'min' in v.keys(): _['schema']['minimum'] = v['min']
			if 'max' in v.keys(): _['schema']['maximum'] = v['max']
			if 'default' in v.keys(): _['schema']['default'] = v['default']
			if 'enum' in v.keys(): _['schema']['enum'] = v['enum']
			if 'required' in v.keys(): _['required'] = v['required']
			parameters.append(_)
		authenticates = []
		if description.auth:
			if description.auth.optional:
				authenticates.append({})
			authenticates.append({description.auth.name: []})
		responses = sorted(description.responses if description.responses else [], key=lambda x: x.status)
		super().__init__(
			operationId=id if id else uuid4().hex,
			summary=description.summary,
			description=description.description,
			tags=description.tags,
			parameters=parameters,
			requestBody={
				'content': {
					content.format : {
						'schema': {'$ref': '#/components/schemas/{}'.format(content.schema.name)} if isinstance(content.schema, Schema) else content.schema,
						'example': content.example,
					} 
					for content in description.body.content
				},
				'description': description.body.description,
				'required': description.body.required,
			} if description.body else {},
			responses={
				str(response.status): Response(response) for response in responses
			} if description.responses else {},
			security=authenticates,
		)
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
