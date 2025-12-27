# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request, Router
from Liquirizia.WSGI.Description import Descriptor, Response, Content

from Liquirizia.Validator import Pattern
from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

from typing import List

__all__ = (
	'RunGet'
)


class SplitHeaders(Pattern):
	def __init__(self, delimiter: str = ','):
		self.delimiter = delimiter
		return
	def __call__(self, parameter: str) -> List[str]:
		parameter = parameter.strip().split(self.delimiter)
		parameter = [item.strip() for item in parameter]
		return parameter


@RequestProperties(
	method='GET',
	url='/options',
	qs=QueryString(
		{
			'p': IsString(),
			'method': Optional(IsString()),
			'headers': Optional(IsString(SplitHeaders(','))),
			'origin': Optional(IsString()),
		},
		requires=('p',),
		format={
			'p': String(format=StringFormat.uri),
			'method': String(enum=('OPTIONS', 'POST', 'GET', 'PATCH', 'PUT', 'DELETE'), required=False),
			'headers': String(required=False),
			'origin': String(required=False),
		},
	),
	response=(
		Response(
			status=200,
			description='성공',
			content=Content(
				format='application/json',
				schema=Object()
			)
		),
		Response(
			status=204,
			description='성공(컨텐츠 없음)',
		),
		Response(
			status=400,
			description='잘못된 요청',
			content=Content(
				format='text/plain',
				schema=String('원인'),
			)
		),
		Response(
			status=404,
			description='찾을 수 없음',
			content=Content(
				format='text/plain',
				schema=String('원인'),
			)
		),
	),
	tags='Common',
)
class RunOptions(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		router = Router()
		descriptor = Descriptor()
		if self.request.uri == '*': 
			return ResponseNoContent(headers={
				'Allow': ', '.join(sorted(list(set(router.methods))))
			})
		path, patterns = router.matches(self.request.qs.p)
		if not patterns:
			raise NotFoundError('{} is not found in router'.format(self.request.qs.p))
		methods = ['OPTIONS']
		methods.extend(patterns.keys())
		if self.request.qs.method and self.request.qs.method != 'OPTIONS':
			if self.request.qs.method not in methods:
				raise NotFoundError('{} is not found in router'.format(self.request.qs.p))
			origins = []
			headers = []
			match = patterns[self.request.qs.method]
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
			if self.request.qs.origin:
				if '*' not in origins and self.request.qs.origin not in origins:
					raise ForbiddenError('Origin {} is not allowed'.format(self.request.qs.origin))
			reqs = self.request.qs.headers
			if reqs:
				missings = [header for header in reqs if header not in headers]
				if missings:
					raise BadRequestError('Unsupported headers: {}'.format(', '.join(missings)))
			doc = descriptor.toDocument(path, self.request.qs.method)
			if doc:
				response = ResponseJSON(doc, headers={
					'Allow': self.request.qs.method,
					'Access-Control-Allow-Methods': self.request.qs.method,
				})
			else:
				response = ResponseNoContent(headers={
					'Allow': self.request.qs.method,
					'Access-Control-Allow-Methods': self.request.qs.method,
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
		reqs = self.request.qs.headers
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
