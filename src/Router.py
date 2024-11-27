# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Route import Route

from .Description import Description
from .Documentation import Document, Information, Path

from re import compile

__all__ = (
	'Router'
)


class Match(object):
	def __init__(self, route, params):
		self.route = route
		self.params = params
		return


class Router(Singleton):
	"""Router"""

	def __init__(self):
		self.routes = []
		self.maps = {}
		self.authes = {}
		self.methods = {'OPTIONS'}
		return

	def matches(self, url: str):
		routes = {}
		
		# find matched list
		for route in self.routes:
			found, params = route.match(url)
			if not found:
				continue
			if route.method not in routes:
				routes[route.method] = []
			routes[route.method].append(Match(route, params))

		# sort ASC by parameter count
		for method in routes.keys():
			routes[method].sort(key=lambda r: len(r.params.keys()))
			routes[method] = routes[method][0]  # select top priority

		return routes

	def add(self, route: Route, description: Description = None):
		self.routes.append(route)
		self.methods.add(route.method)
		if not description: return
		regex = compile(r':(\w+)')
		url = regex.sub(r"{\1}", route.url)
		if url not in self.maps:
			self.maps[url] = {}
		self.maps[url][route.method.lower()] = Path(description)
		if description.auth:
			if description.auth.name not in self.authes.keys():
				self.authes[description.auth.name] = description.auth.format
			else:
				fmt = dict(self.authes[description.auth.name])
				fmt.update(description.auth.format)
				self.authes[description.auth.name] = fmt
		return
	
	def toDocument(self, info: Information, version: str = '3.1.0'):
		ORDER = {
			'OPTIONS': '00',
			'POST': '10',
			'HEAD': '11',
			'GET': '12',
			'PUT': '13',
			'DELETE': '14',
			'TRACE': '20',
			'PATCH': '30',
		}
		for k, v in self.maps.items():
			self.maps[k] = dict(sorted(self.maps[k].items(), key=lambda _: ORDER.get(_[0].upper(), '99')))
		self.maps = dict(sorted(self.maps.items(), key=lambda _: _[0]))
		return Document(info=info, version=version, routes=self.maps, authenticates=self.authes)
