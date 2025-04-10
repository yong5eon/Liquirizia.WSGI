# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Description import (
	Description,
	Response,
	Content,
)
from .Document import (
	Document,
	Information,
	Path,
	Tag,
)
from Liquirizia.Description import *

from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from re import compile
from typing import Sequence, Any, List, Iterable

__all__ = (
	'Descriptor',
)

class SortKey(metaclass=ABCMeta):
	@abstractmethod
	def __call__(self, o: Any) -> Any:
		raise NotImplementedError('{} must be implemented __call__'.format(self.__class__.__name__))
	
class Url(SortKey):
	def __call__(self, o: str) -> str:
		return o

class Method(SortKey):
	def __call__(self, o: str) -> str:
		return {
			'OPTIONS': '00',
			'CONNECT': '10',
			'POST': '21',
			'HEAD': '30',
			'GET': '31',
			'PUT': '41',
			'PATCH': '42',
			'TRACE': '50',
			'DELETE': '71',
		}.get(o.upper(), '99')


class Descriptor(Singleton):
	"""Descriptor Class"""
	def __init__(
		self,
		info: Information = Information(),
		version: str = '3.1.0',
		errorResponses: List[Response] = None,
		authErrorResponses: List[Response] = None,
	):
		self.infomation = info
		self.version = version
		self.maps = {}
		self.authes = {}
		self.errors = errorResponses if errorResponses else []
		if not isinstance(self.errors, Iterable):
			self.errors = [self.errors]
		self.errors = [*self.errors]
		self.authErrors = authErrorResponses if authErrorResponses else []
		if not isinstance(self.authErrors, Iterable):
			self.authErrors = [self.authErrors]
		self.authErrors = [*self.authErrors]
		return

	def add(
		self,
		description: Description,
	) -> 'Descriptor':
		if description.url not in self.maps:
			self.maps[description.url] = []
		if description.auth and self.authErrors:
			if not description.responses:
				description.responses = []
			description.responses.extend(self.authErrors)
		if self.errors:
			if not description.responses:
				description.responses = []
			description.responses.extend(self.errors)
		self.maps[description.url].append((
			description.method.lower(),
			Path(description),
		))
		if description.auth:
			if description.auth.name not in self.authes.keys():
				self.authes[description.auth.name] = description.auth.format
			else:
				fmt = dict(self.authes[description.auth.name])
				fmt.update(description.auth.format)
				self.authes[description.auth.name] = fmt
		return self
	
	def addErrorResponse(self, response: Response) -> 'Descriptor':
		self.errors.append(response)
		return self
	
	def addAuthErrorResponse(self, response: Response) -> 'Descriptor':
		self.authErrors.append(response)
		return self

	def toDocument(
		self,
		url: str = None,
		method: str = None,
		tags: Sequence[Tag] = None,
		schemas: Sequence[Schema] = None,
		sortUrl: SortKey = Url(),
		sortMethod: SortKey = Method(),
	) -> Document:
		regex = compile(r':(\w+)')
		routes = []
		def cpr(o):
			key, desc = o
			return sortUrl(key)
		def cpp(o):
			m, path = o
			return sortMethod(m)
		if url:
			if url in self.maps.keys():
				p= regex.sub(r"{\1}", url)
				ps = OrderedDict()
				for m, path in sorted(self.maps[url], key=cpp):
					if method and m != method.lower():
						continue
					ps[m] = path
				routes.append((p, ps))
			else:
				return None
		else:
			for p, desc in sorted(self.maps.items(), key=cpr):
				p= regex.sub(r"{\1}", p)
				ps = OrderedDict()
				for m, path in sorted(desc, key=cpp):
					ps[m] = path
				routes.append((p, ps))
		formats = {schema.name: schema.format for schema in schemas} if schemas else {}
		return Document(
			info=self.infomation,
			version=self.version,
			routes=OrderedDict(routes),
			schemas=formats,
			authenticates=self.authes,
			tags=tags,
		)
