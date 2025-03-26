# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Description import (
	Description,
)
from .Documentation import (
	Document,
	Information,
	Path,
	Tag,
)
from .Value import Schema

from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from re import compile
from typing import Sequence, Any

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
	def __init__(self, info: Information, version: str = '3.1.0'):
		self.infomation = info
		self.version = version
		self.maps = {}
		self.authes = {}
		return

	def add(
		self,
		description: Description,
	) -> 'Descriptor':
		if description.url not in self.maps:
			self.maps[description.url] = []
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

	def toDocument(
		self,
		tags: Sequence[Tag] = None,
		schemas: Sequence[Schema] = None,
		url: SortKey = Url(),
		method: SortKey = Method(),
	) -> Document:
		regex = compile(r':(\w+)')
		routes = []
		def cpr(o):
			key, desc = o
			return url(key)
		def cpp(o):
			m, path = o
			return method(m)
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
