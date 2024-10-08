# -*- coding: utf-8 -*-

from .Documentation import Documentation

from .Information import (
	Information,
)

from ..Description import (
	Description,
	DescriptionResponse,
	DescriptionResponseBody,
	DescriptionResponseHeader,
)

from uuid import uuid4

from typing import Mapping, Optional

__all__ = (
	'Document',
	'Path',
)


class ResponseHeader(Documentation):
	def __init__(self, header: DescriptionResponseHeader):
		super().__init__(
			description=header.description,
			schema={
				'type': header.type,
				'format': header.format,
				'minimum': header.min,
				'maximum': header.max,
				'default': header.default,
				'enum': header.ins,
			},
			required=header.required,
			deprecated=header.deprecated,
		)
		return
	
class ResponseBody(Documentation):
	def __init__(
		self,
		body: DescriptionResponseBody
	):
		super().__init__(
			schema=body.content,
			example=body.example,
		)
		return


class Response(Documentation):
	def __init__(self, response: DescriptionResponse):
		super().__init__(
			description=response.description,
			content={
				body.format: ResponseBody(body) for body in response.body
			} if response.body else {},
			headers={
				header.name: ResponseHeader(header) for header in response.headers
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
		for parameter in description.parameter if description.parameter else []:
			parameters.append({
					'name': parameter.name,
					'in': 'path',
					'description': parameter.description,
					'schema': {
						'type': parameter.type,
						'format': parameter.format,
						'minimum': parameter.min,
						'maximum': parameter.max,
						'default': parameter.default,
						'enum': parameter.ins,
					},
					'required': parameter.required,
					'deprecated': parameter.deprecated,
				})
		for header in description.header if description.header else []:
			parameters.append({
					'name': header.name,
					'in': 'header',
					'description': header.description,
					'schema': {
						'type': header.type,
						'format': header.format,
						'minimum': header.min,
						'maximum': header.max,
						'default': header.default,
						'enum': header.ins,
					},
					'required': header.required,
					'deprecated': header.deprecated,
				})
		for q in description.qs if description.qs else []:
			parameters.append({
					'name': q.name,
					'in': 'query',
					'description': q.description,
					'schema': {
						'type': q.type,
						'format': q.format,
						'minimum': q.min,
						'maximum': q.max,
						'default': q.default,
						'enum': q.ins,
					},
					'required': q.required,
					'deprecated': q.deprecated,
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
					content.format: {
						'schema': content.content,
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