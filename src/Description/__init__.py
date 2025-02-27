# -*- coding: utf-8 -*-

from ..Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestServerSentEventsRunner,
	RequestWebSocketRunner,
)
from .Types import (
	Value,
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
		parameters: Optional[Dict[str, Value]] = None,
		headers: Optional[Dict[str, Value]] = None,
		qs: Optional[Dict[str, Value]] = None,
		body: Body = None,
		responses: Optional[Union[Response,Sequence[Response]]] = None,
		auth: Auth = None,
		tags: Optional[Union[str, Sequence[str]]] = None,
		order: Union[int, float, str] = 0,
	):
		self.description = Description(
			summary=summary,
			description=description,
			parameters=parameters,
			headers=headers,
			qs=qs,
			body=body,
			responses=responses,
			auth=auth,
			tags=tags,
			order=order,
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
		descriptor = Descriptor()
		descriptor.add(
			obj=obj,
			description=self.description,
		)
		return obj
