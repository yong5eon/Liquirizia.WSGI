# -*- coding: utf-8 -*-

from ..RequestFactory import RequestFactory
from ..Request import Request
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..Router import Router
from ..Errors import *
from ..Responses import *
from ..Description import Descriptor

__all__ = (
	'RouteOptions'
)


class RouteOptions(RequestFactory):
	"""Route Options Class"""
	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		router = Router()
		descriptor = Descriptor()
		if request.uri == '*': 
			writer.response(ResponseNoContent(headers={
				'Allow': ', '.join(sorted(list(set(router.methods))))
			}))
			return
		path, patterns = router.matches(request.uri)
		if not patterns:
			raise NotFoundError('{} is not found in router'.format(request.uri))
		methods = ['OPTIONS']
		methods.extend(patterns.keys())
		if request.header('Access-Control-Request-Method') and request.header('Access-Control-Request-Method') != 'OPTIONS':
			if request.header('Access-Control-Request-Method') not in methods:
				raise NotFoundError('{} is not found in router'.format(request.uri))
			origins = []
			headers = []
			match = patterns[request.header('Access-Control-Request-Method')]
			route = match.route
			if hasattr(route, 'origin'):
				if route.origin:
					if route.origin.all:
						origins.append('*')
					else:
						origins.extend(route.origin.matches)
			if hasattr(route, 'auth'):
				if route.auth:
					headers.append('Authorization')
			if hasattr(route, 'header'):
				if route.header:
					headers.extend(route.header.headers)
			if hasattr(route, 'body'):
				if route.body:
					headers.append('Content-Type')
			origins = list(set(origins))
			headers = list(set(headers))
			if request.header('Origin'):
				if '*' not in origins and request.header('Origin') not in origins:
					raise ForbiddenError('Origin {} is not allowed'.format(request.header('Origin')))
			reqs = request.header('Access-Control-Request-Headers')
			if reqs:
				missings = [header for header in reqs if header not in headers]
				if missings:
					raise BadRequestError('Unsupported headers: {}'.format(', '.join(missings)))
			doc = descriptor.toDocument(path, request.header('Access-Control-Request-Method'))
			if doc:
				response = ResponseJSON(doc, headers={
					'Allow': request.header('Access-Control-Request-Method'),
					'Access-Control-Allow-Methods': request.header('Access-Control-Request-Method'),
				})
			else:
				response = ResponseNoContent(headers={
					'Allow': request.header('Access-Control-Request-Method'),
					'Access-Control-Allow-Methods': request.header('Access-Control-Request-Method'),
				})
			if origins:
				response.header('Access-Control-Allow-Origin', ', '.join(origins))
			if headers:
				response.header('Access-Control-Allow-Headers', ', '.join(headers))
			return response
		origins = []
		headers = []
		for _, match in patterns.items():
			route = match.route
			if hasattr(route, 'origin'):
				if route.origin:
					if route.origin.all:
						origins.append('*')
					else:
						origins.extend(route.origin.matches)
			if hasattr(route, 'auth'):
				if route.auth:
					headers.append('Authorization')
			if hasattr(route, 'header'):
				if route.header:
					headers.extend(route.header.headers)
			if hasattr(route, 'body'):
				if route.body:
					headers.append('Content-Type')
		origins = list(set(origins))
		headers = list(set(headers))
		reqs = request.header('Access-Control-Request-Headers')
		if reqs:
			missings = [header for header in reqs if header not in headers]
			if missings:
				raise BadRequestError('Unsupported headers: {}'.format(', '.join(missings)))
		doc = descriptor.toDocument(
			path, 
			sortMethod=lambda o: {
				'POST': 1,
				'GET': 2,
				'PUT': 3,
				'DELETE': 4,
			}.get(o.upper(), 9)
		)
		if doc:
			response = ResponseJSON(doc, headers={
				'Allow': ', '.join(methods),
				'Access-Control-Allow-Methods': ', '.join(methods),
			})
		else:
			response = ResponseNoContent(headers={
				'Allow': ', '.join(methods),
				'Access-Control-Allow-Methods': ', '.join(methods),
			})
		if origins:
			response.header('Access-Control-Allow-Origin', ', '.join(origins))
		if headers:
			response.header('Access-Control-Allow-Headers', ', '.join(headers))
		return response
