# -*- coding: utf-8 -*-

from ..Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestServerSentEventsRunner,
	RequestWebSocketRunner,
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
	Header,
	Query,
	Cookie,
	TLS,
	OpenIdConnect,
)
from .Document import (
	Document,
	Path,
	Information,
	Contact,
	License,
	Tag,
)

from Liquirizia.Description import Value, Schema
from typing import Type, Union, Optional, Sequence, Dict

__all__ = (
	# Decorator
	'RequestDescription',
	# Descriptor
	'Descriptor',
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
	'Header',
	'Query',
	'Cookie',
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
		descriptor = Descriptor()
		descriptor.add(self.description)
		return obj
