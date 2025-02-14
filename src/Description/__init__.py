# -*- coding: utf-8 -*-

from .Description import (
	Description,
	DescriptionRequestParameter,
	DescriptionRequestHeader,
	DescriptionRequestQueryString,
	DescriptionRequestBody,
	DescriptionRequestBodyProperties,
	DescriptionRequestAuth,
	DescriptionResponse,
	DescriptionResponseHeader,
	DescriptionResponseBody,
	DescriptionResponseBodyExample,
	Property,
	PropertyType,
	Value,
	ValueType,
	Object,
	ObjectProperties,
)
from .Model import (
	Boolean,
	Integer,
	Number,
	String,
	Array,
)
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

from .Descriptor import Descriptor
from .Documentation import (
	Information,
	Contact,
)

from ..Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestServerSentEventsRunner,
	RequestWebSocketRunner,
)

from typing import Type, Union, Optional, Sequence

__all__ = (
	## Description
	'Description',
	'DescriptionRequestParameter',
	'DescriptionRequestHeader',
	'DescriptionRequestQueryString',
	'DescriptionRequestBody',
	'DescriptionRequestBodyProperties',
	'DescriptionRequestAuth',
	'DescriptionResponse',
	'DescriptionResponseHeader',
	'DescriptionResponseBody',
	'DescriptionResponseBodyExample',
	# Property
	'Property',
	'PropertyType',
	# Model
	'Value',
	'ValueType',
	'Object',
	'ObjectProperties',
	'Boolean',
	'Integer',
	'Number',
	'String',
	'Array',
	# Auth
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
	# Descriptor
	'Descriptor',
	# Documentation
	'Information',
	'Contact',
	# Decorator
	'RequestDescription',
)


class RequestDescription(object):
	def __init__(
		self,
		summary: str,
		description: str,
		parameters: Optional[Union[DescriptionRequestParameter,Sequence[DescriptionRequestParameter]]] = None,
		headers: Optional[Union[DescriptionRequestHeader,Sequence[DescriptionRequestHeader]]] = None,
		qs: Optional[Union[DescriptionRequestQueryString,Sequence[DescriptionRequestQueryString]]] = None,
		body: DescriptionRequestBodyProperties = None,
		responses: Optional[Union[DescriptionResponse,Sequence[DescriptionResponse]]] = None,
		auth: DescriptionRequestAuth = None,
		tags: Optional[Union[str, Sequence[str]]] = None,
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
			tags=tags
		)
		return
	def __call__(self, obj: Type[Union[RequestRunner,RequestStreamRunner,RequestServerSentEventsRunner,RequestWebSocketRunner]]):
		descriptor = Descriptor()
		descriptor.add(
			obj=obj,
			description=self.description,
		)
		return obj
