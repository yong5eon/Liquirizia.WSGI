# -*- coding: utf-8 -*-

from .Documentation import Documentation

from .Information import (
	Information,
)

from ..Description import (
	Description,
	Response as ResponseDescription,
	Body as BodyDescription,
)
from ..Types import Value

from uuid import uuid4

from typing import Mapping, Optional

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
	
class ResponseBody(Documentation):
	def __init__(
		self,
		body: BodyDescription
	):
		super().__init__(
			schema=body.schema,
		)
		return


class Response(Documentation):
	def __init__(self, response: ResponseDescription):
		super().__init__(
			description=response.description,
			content={
				content.format: ResponseBody(content) for content in response.content
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
			parameters.append({
				'name': k,
				'in': 'path',
				'description': v['description'] if 'description' in v.keys() else None,
				'schema': {
					'type': v['type'] if 'type' in v.keys() else None,
					'format': v['format'] if 'format' in v.keys() else None,
					'minimum': v['min'] if 'min' in v.keys() else None,
					'maximum': v['max'] if 'max' in v.keys() else None,
					'default': v['default'] if 'default' in v.keys() else None,
					'enum': v['enum'] if 'enum' in v.keys() else None,
				},
				'required': v['required'] if 'required' in v.keys() else None,
				'deprecated': v['deprecated'] if 'deprecated' in v.keys() else None,
			})
		for k, v in description.headers.items() if description.headers else []:
			parameters.append({
				'name': k,
				'in': 'header',
				'description': v['description'] if 'description' in v.keys() else None,
				'schema': {
					'type': v['type'] if 'type' in v.keys() else None,
					'format': v['format'] if 'format' in v.keys() else None,
					'minimum': v['min'] if 'min' in v.keys() else None,
					'maximum': v['max'] if 'max' in v.keys() else None,
					'default': v['default'] if 'default' in v.keys() else None,
					'enum': v['enum'] if 'enum' in v.keys() else None,
				},
				'required': v['required'] if 'required' in v.keys() else None,
				'deprecated': v['deprecated'] if 'deprecated' in v.keys() else None,
			})
		for k, v in description.qs.items() if description.qs else []:
			parameters.append({
				'name': k,
				'in': 'query',
				'description': v['description'] if 'description' in v.keys() else None,
				'schema': {
					'type': v['type'] if 'type' in v.keys() else None,
					'format': v['format'] if 'format' in v.keys() else None,
					'minimum': v['min'] if 'min' in v.keys() else None,
					'maximum': v['max'] if 'max' in v.keys() else None,
					'default': v['default'] if 'default' in v.keys() else None,
					'enum': v['enum'] if 'enum' in v.keys() else None,
				},
				'required': v['required'] if 'required' in v.keys() else None,
				'deprecated': v['deprecated'] if 'deprecated' in v.keys() else None,
			})
		authenticates = []
		if description.auth:
			if description.auth.optional:
				authenticates.append({})
			authenticates.append({description.auth.name: []})
		super().__init__(
			summary=description.summary,
			description=description.description,
			operationId=id if id else uuid4().hex,
			tags=description.tags,
			responses={
				str(response.status): Response(response) for response in description.responses
			} if description.responses else {},
			parameters=parameters,
			requestBody={
				'content': {
					content.format : {
						'schema': content.schema,
						'example': content.example,
					} 
					for content in description.body.content
				},
				'description': description.body.description,
				'required': description.body.required,
			} if description.body else {},
			security=authenticates,
		)
		return


class Document(Documentation):
	def __init__(
		self,
		info: Information,
		version='3.1.0',
		routes: Optional[Mapping[str, Mapping[str, Path]]] = None,
		authenticates: Optional[Mapping[str, Mapping]]= None,
	):
		self.__document__ = {
			'openapi': version,
			'info': info,
			'components': {}
		}
		if routes:
			self.__document__['paths'] = routes
		self.__document__['components']['securitySchemes'] = authenticates
		return
