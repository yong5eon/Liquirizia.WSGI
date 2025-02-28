# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Description import (
	Description,
	Schema,
)
from .Documentation import (
	Document,
	Information,
	Path,
	Tag,
)

from collections import OrderedDict
from re import compile

from typing import Sequence

__all__ = (
	'Descriptor',
)


class Descriptor(Singleton):
	"""Descriptor Class"""
	def __init__(self, info: Information, version: str = '3.1.0'):
		self.infomation = info
		self.version = version
		self.maps = {}
		self.schemas = {}
		self.authes = {}
		return

	def add(
		self,
		description: Description,
	) -> 'Descriptor':
		regex = compile(r':(\w+)')
		url = regex.sub(r"{\1}", description.url)
		if url not in self.maps:
			self.maps[url] = []
		self.maps[url].append((
			description.method.lower(),
			description.order,
			Path(description),
		))
		for content in description.body.content if description.body and description.body.content else []:
			if isinstance(content.schema, Schema):
				self.schemas[content.schema.name] = content.schema.format
		for response in description.responses if description.responses else []:
			for content in response.content if response.content else []:
				if isinstance(content.schema, Schema):
					self.schemas[content.schema.name] = content.schema.format
		if description.auth:
			if description.auth.name not in self.authes.keys():
				self.authes[description.auth.name] = description.auth.format
			else:
				fmt = dict(self.authes[description.auth.name])
				fmt.update(description.auth.format)
				self.authes[description.auth.name] = fmt
		return self

	def toDocument(self, tags: Sequence[Tag] = None) -> Document:
		routes = []
		def cpr(o):
			key, paths = o
			if paths[0][1]:
				return str(paths[0][1])
			return str(key)
		def cpp(o):
			method, order, path = o
			if order: return str(order)
			return str(method)
		for k, paths in sorted(self.maps.items(), key=cpr):
			ps = {}
			for method, order, path in sorted(paths, key=cpp):
				ps[method] = path
			routes.append((k, ps))
		schemas = OrderedDict(sorted(self.schemas.items(), key=lambda x: x[0]))
		return Document(
			info=self.infomation,
			version=self.version,
			routes=OrderedDict(routes),
			schemas=schemas,
			authenticates=self.authes,
			tags=tags,
		)
