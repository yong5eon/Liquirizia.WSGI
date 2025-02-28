# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Description import Description
from .Documentation import (
	Document,
	Information,
	Path as PathInformation,
	Tag,
)

from ..Properties import (
	RequestRunner,
	RequestStreamRunner,
	RequestServerSentEventsRunner,
	RequestWebSocketRunner,
)

from collections import OrderedDict
from re import compile
from os.path import splitext, split
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib import import_module
from pkgutil import walk_packages

from typing import Type, Union, Sequence

__all__ = (
	'Descriptor',
)


class Descriptor(Singleton):
	def __init__(self, info: Information, version: str = '3.1.0'):
		self.infomation = info
		self.version = version
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
			self.maps[url] = []
		self.maps[url].append((
			obj.__properties__.method.lower(),
			description.order,
			PathInformation(description),
		))
		if description.auth:
			if description.auth.name not in self.authes.keys():
				self.authes[description.auth.name] = description.auth.format
			else:
				fmt = dict(self.authes[description.auth.name])
				fmt.update(description.auth.format)
				self.authes[description.auth.name] = fmt
		return self

	def toDocument(self, tags: Sequence[Tag] = None) -> Document:
		_ = []
		for k, paths in sorted(self.maps.items(), key=lambda x: x[1][0][1]):
			ps = {}
			for method, order, path in sorted(paths, key=lambda x: x[1]):
				ps[method] = path
			_.append((k, ps))
		return Document(info=self.infomation, version=self.version, routes=OrderedDict(_), authenticates=self.authes, tags=tags)

	def load(self, mod: str = None, path: str = None, ext: str = 'py'):
		if mod:
			self.loadModule(mod)
		if path:
			ps = Path(path).rglob('*.{}'.format(ext))
			for p in ps if ps else []:
				p = self.loadPath(str(p))
		return
	
	def loadPath(self, path):
		head, tail = split(path)
		file, ext = splitext(tail)
		head = head.replace('\\', '.').replace('/', '.')
		mod = '{}.{}'.format(head, file)
		loader = SourceFileLoader(mod, path)
		mo = loader.load_module()
		if not mo:
			return None
		return mo
	
	def loadModule(self, mod):
		pkg = import_module(mod)
		for _, name, isPackage in walk_packages(pkg.__path__):
			fullname = pkg.__name__ + '.' + name
			if isPackage:
				self.loadModule(fullname)
				continue
			import_module(fullname)
		return
