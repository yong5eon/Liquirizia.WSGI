# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Description import Description
from .Documentation import Document, Information, Path

from ..Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestServerSentEventsRunner,
	RequestWebSocketRunner,
)

from collections import OrderedDict
from re import compile
from typing import Type, Union

__all__ = (
	'Descriptor',
)


class Descriptor(Singleton):
	def __init__(self):
		self.maps = {}
		self.authes = {}
		return
	def add(
		self,
		obj: Type[Union[
			RequestRunner,
			RequestStreamRunner,
			RequestServerSentEventsRunner,
			RequestWebSocketRunner,
		]],
		description: Description,
	) -> 'Descriptor':
		if not obj.__properties__:
			raise RuntimeError('{} must be decorated with RequestProperties'.format(obj.__name__))
		regex = compile(r':(\w+)')
		url = regex.sub(r"{\1}", obj.__properties__.url)
		if url not in self.maps:
			self.maps[url] = {}
		self.maps[url][obj.__properties__.method.lower()] = Path(description)
		if description.auth:
			if description.auth.name not in self.authes.keys():
				self.authes[description.auth.name] = description.auth.format
			else:
				fmt = dict(self.authes[description.auth.name])
				fmt.update(description.auth.format)
				self.authes[description.auth.name] = fmt
		return self

	def toDocument(self, info: Information, version: str = '3.1.0'):
		ORDER = {
			'OPTIONS': '00',
			'CONNECT': '11',
			'TRACE': '12',
			'POST': '21',
			'HEAD': '22',
			'GET': '23',
			'PUT': '24',
			'PATCH': '25',
			'DELETE': '26',
		}
		# TODO : fix order
		maps = {}
		for k, _ in self.maps.items():
			maps[k] = OrderedDict(sorted(self.maps[k].items(), key=lambda _: ORDER.get(_[0].upper(), '99')))
		maps = OrderedDict(sorted(self.maps.items(), key=lambda _: _[0]))
		return Document(info=info, version=version, routes=maps, authenticates=self.authes)
