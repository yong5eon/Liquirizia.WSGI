# -*- coding: utf-8 -*-

from .Property import (
	Type as PropertyType,
	Property,
)
from .Model import (
	Type as ValueType,
	Value,
	Object,
	ObjectProperties,
)

from typing import Any
from typing import Optional, Union, Sequence, Mapping

__all__ = (
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
	'Value',
	'ValueType',
	'Object',
	'ObjectProperties',
	'Property',
	'PropertyType',
)

class DescriptionResponseBodyExample(object):
	def __init__(
		self,
		name: str,
		value: Any,
		description: Optional[str] = None,
		summary: Optional[str] = None,
	):
		self.name = name
		self.value = value
		self.description = description
		self.summary = summary
		return
	
class DescriptionResponseBody(object):
	def __init__(
		self,
		format: str,
		content: Object = None,
		example: Any = None,
	):
		self.format = format
		self.content = content
		self.example = example
		return
	

class DescriptionResponseHeader(Property): pass

class DescriptionResponse(object):
	def __init__(
		self,
		status: int,
		description: str,
		body: Optional[Union[DescriptionResponseBody, Sequence[DescriptionResponseBody]]] = None,
		headers: Optional[Mapping[str, DescriptionResponseHeader]] = None,
	):
		self.status = status
		self.description = description
		self.body = body
		if self.body:
			if not isinstance(self.body, Sequence):
				self.body = [self.body]
		self.headers = headers
		if self.headers:
			if not isinstance(self.headers, Sequence):
				self.headers = [self.headers]
		return

class DescriptionRequestBody(object):
	def __init__(
		self,
		format: str,
		content: Object,
		example: Any = None,
	):
		self.format = format
		self.content = content
		self.example = example
		return
	
class DescriptionRequestBodyProperties(object):
	def __init__(
		self,
		content: Optional[Union[DescriptionRequestBody,Sequence[DescriptionRequestBody]]]= None,
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

class DescriptionRequestParameter(Property): pass
class DescriptionRequestHeader(Property): pass
class DescriptionRequestQueryString(Property): pass

class DescriptionRequestAuth(object):
	def __init__(
		self,
		name: str,
		format: Any = None,
		optional: bool = False,
	):
		self.name = name
		self.format = format
		self.optional = optional
		return

class Description(object):
	def __init__(
		self,
		description: str,
		summary: str,
		responses: Optional[Union[DescriptionResponse,Sequence[DescriptionResponse]]] = None,
		parameter: Optional[Union[DescriptionRequestParameter,Sequence[DescriptionRequestParameter]]] = None,
		header: Optional[Union[DescriptionRequestHeader,Sequence[DescriptionRequestHeader]]] = None,
		qs: Optional[Union[DescriptionRequestQueryString,Sequence[DescriptionRequestQueryString]]] = None,
		body: DescriptionRequestBodyProperties = None,
		auth: DescriptionRequestAuth = None,
		tags: Optional[Union[str, Sequence[str]]] = None,
	):
		self.description = description
		self.summary = summary
		self.tags = tags
		if self.tags:
			if isinstance(self.tags, str):
				self.tags = [self.tags]
		self.responses = responses
		if self.responses:
			if not isinstance(self.responses, Sequence):
				self.responses = [self.responses]
		self.parameter = parameter
		if self.parameter:
			if not isinstance(self.parameter, Sequence):
				self.parameter = [self.parameter]
		self.header = header
		if self.header:
			if not isinstance(self.header, Sequence):
				self.header = [self.header]
		self.qs = qs
		if self.qs:
			if not isinstance(self.qs, Sequence):
				self.qs = [self.qs]
		self.body = body
		self.auth = auth
		return