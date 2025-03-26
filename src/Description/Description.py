# -*- coding: utf-8 -*-

from .Value import Value, Schema
from .Auth import Authorization

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
		content: Optional[Union[Content,Sequence[Content]]]= None,
		description: str = None,
		required: bool = True,
	):
		self.content = content
		if self.content:
			if not isinstance(self.content, Sequence):
				self.content = [self.content]
		self.description = description
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
		format: Authorization = None,
		optional: bool = False,
	):
		self.name = name
		self.format = format
		self.optional = optional
		return


class Description(object):
	def __init__(
		self,
		summary: str,
		description: str,
		tags: Optional[Union[str, Sequence[str]]] = None,
		method: str = None,
		url: str = None,
		parameters: Optional[Dict[str, Value]] = None,
		headers: Optional[Dict[str, Value]] = None,
		qs: Optional[Dict[str, Value]] = None,
		body: Body = None,
		responses: Optional[Union[Response,Sequence[Response]]] = None,
		auth: Auth = None,
	):
		self.summary = summary
		self.description = description
		self.tags = tags
		if self.tags:
			if isinstance(self.tags, str):
				self.tags = [self.tags]
		self.method = method
		self.url = url
		self.parameters = parameters
		self.headers = headers
		self.qs = qs
		self.body = body
		self.responses = responses
		if self.responses:
			if not isinstance(self.responses, Sequence):
				self.responses = [self.responses]
		self.auth = auth
		return
