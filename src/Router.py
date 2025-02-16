# -*- coding: utf-8 -*-

from Liquirizia.Template import Singleton

from .Route import Route

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

	def add(self, route: Route):
		self.routes.append(route)
		self.methods.add(route.method)
		return
