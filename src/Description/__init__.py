# -*- coding: utf-8 -*-

from ..Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestServerSentEventsRunner,
	RequestWebSocketRunner,
)
from .Value import (
	Value,
	Schema,
)
from .Types import (
	Boolean,
	Integer,
	Number,
	String,
	Array,
	Object,
	ObjectProperties,
)
from .Description import (
	Description,
	Content,
	Body,
	Auth,
	Response,
)
from .Descriptor import Descriptor
from .Auth import (
	OAuth2Password,
	OAuth2Implict,
	OAuth2Credentials,
	OAuth2Code,
	HTTP,
	KeyHeader,
	KeyQuery,
	KeyCookie,
	TLS,
	OpenIdConnect,
)
from .Documentation import (
	Document,
	Path,
	Information,
	Contact,
	License,
	Tag,
)

from typing import Type, Union, Optional, Sequence, Dict

__all__ = (
	# Decorator
	'RequestDescription',
	# Descriptor
	'Descriptor',
	# Value
	'Value',
	'Schema',
	# Types
	'Boolean',
	'Integer',
	'Number',
	'String',
	'Array',
	'Object',
	'ObjectProperties',
	# Description
	'Description',
	'Schema',
	'Content',
	'Body',
	'Auth',
	'Response',
	# Authorization
	'OAuth2Password',
	'OAuth2Implict',
	'OAuth2Credentials',
	'OAuth2Code',
	'HTTP',
	'KeyHeader',
	'KeyQuery',
	'KeyCookie',
	'TLS',
	'OpenIdConnect',
	# Documentation
	'Document',
	'Path',
	'Information',
	'Contact',
	'License',
	'Tag',
)


class RequestDescription(object):
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
		self.description = Description(
			summary=summary,
			description=description,
			tags=tags,
			method=method,
			url=url,
			parameters=parameters,
			headers=headers,
			qs=qs,
			body=body,
			responses=responses,
			auth=auth,
		)
		return
	def __call__(
		self,
		obj: Type[Union[
			RequestRunner,
			RequestStreamRunner,
			RequestServerSentEventsRunner,
			RequestWebSocketRunner
		]]):
		if not self.description.method or not self.description.url:
			self.description.method = obj.__properties__.method
			self.description.url = obj.__properties__.url
		if not self.description.method:
			raise RuntimeError('Method is required')
		if not self.description.url:
			raise RuntimeError('URL is required')
		descriptor = Descriptor()
		descriptor.add(self.description)
		return obj
