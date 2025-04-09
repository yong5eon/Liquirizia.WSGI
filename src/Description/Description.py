# -*- coding: utf-8 -*-

from .Auth import Authenticate

from Liquirizia.Description import Value, Schema
from typing import Optional, Union, Sequence, Dict, Any

__all__ = (
	'Description',
	'Auth',
	'Response',
	'Body',
	'Content',
)


class Content(object):
	def __init__(
		self,
		format: str,
		schema: Optional[Union[Value, Schema]] = None,
		example: Optional[Any] = None,
	):
		self.format = format
		self.schema = schema 
		self.example = example
		return


class Body(object):
	def __init__(
		self,
		description: str = None,
		content: Optional[Union[Content,Sequence[Content]]]= None,
		required: bool = True,
	):
		self.description = description
		self.content = content
		if self.content:
			if not isinstance(self.content, Sequence):
				self.content = [self.content]
		self.required = required
		return


class Response(object):
	def __init__(
		self,
		status: int,
		description: str,
		content: Optional[Union[Content, Sequence[Content]]] = None,
		headers: Optional[Dict[str, Value]] = None,
	):
		self.status = status
		self.description = description
		self.content = content
		if self.content:
			if not isinstance(self.content, Sequence):
				self.content = [self.content]
		self.headers = headers
		return


class Auth(object):
	def __init__(
		self,
		name: str,
		format: Authenticate = None,
		optional: bool = False,
	):
		self.name = name
		self.format = format
		self.optional = optional
		return


class Description(object):
	def __init__(
		self,
		method: str = None,
		url: str = None,
		auth: Auth = None,
		parameters: Optional[Dict[str, Value]] = None,
		qs: Optional[Dict[str, Value]] = None,
		headers: Optional[Dict[str, Value]] = None,
		body: Body = None,
		responses: Optional[Union[Response,Sequence[Response]]] = None,
		summary: str = None,
		description: str = None,
		tags: Optional[Union[str, Sequence[str]]] = None,
	):
		self.method = method
		self.url = url
		self.auth = auth
		self.parameters = parameters
		self.qs = qs
		self.headers = headers
		self.body = body
		self.responses = responses
		if self.responses:
			if not isinstance(self.responses, Sequence):
				self.responses = [self.responses]
		self.summary = summary
		self.description = description
		self.tags = tags
		if self.tags:
			if isinstance(self.tags, str):
				self.tags = [self.tags]
		return
