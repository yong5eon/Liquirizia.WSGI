# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Properties.Validator import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request, Router
from Liquirizia.WSGI.Description import Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

__all__ = (
	'RunGet'
)


@RequestProperties(
	method='GET',
	url='/options',
	qs=QueryString(
		{
			'p': IsString(error=BadRequestError('경로(p) 는 문자열을 필요로 합니다')),
		},
		requires=('p',),
		requiresError=BadRequestError('질의에 경로(p) 는 필수 입니다.'),
		format={
			'p': String(format=StringFormat.uri),
		},
	),
	header=Header(
		{
			'Access-Control-Request-Method': IsToNone(IsString()),
			'Access-Control-Request-Headers': IsToNone(IsString()),
		},
		format={
			'Access-Control-Request-Method': String(required=False),
			'Access-Control-Request-Headers': String(required=False),
		}
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
	tags='ETC',
)
class RunOptions(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		# TODO : implement OPTIONS
		router = Router()
		if self.request.uri == '*': 
			return ResponseNoContent(headers={
				'Allow': ', '.join(sorted(list(set(router.methods))))
			})
		_, patterns = router.matches(self.request.qs.p)
		if not patterns:
			raise NotFoundError('{} is not found in router'.format(self.request.qs.p))
		methods = ['OPTIONS']
		methods.extend(patterns.keys())
		if self.request.header('Access-Control-Request-Method'):
			if self.request.header('Access-Control-Request-Method') not in methods:
				raise NotFoundError('{} is not found in router'.format(self.request.qs.p))
			# TODO : 해당 메소드에 대한 지원 처리
			pass
		response = ResponseNoContent(headers={
			'Allow': ', '.join(methods),
			'Access-Control-Allow-Methods': ', '.join(methods),
		})
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
					origins.append('Authroization')
			if hasattr(route, 'header'):
				if route.header:
					origins.extend(route.header.headers)
			if hasattr(route, 'body'):
				if route.body:
					origins.append('Content-Type')
		origins = list(set(origins))
		if origins:
			response.header('Access-Control-Allow-Origin', ', '.join(origins))
		headers = list(set(headers))
		if headers:
			response.header('Access-Control-Allow-Headers', ', '.join(headers))
		if self.request.header('Access-Control-Request-Headers'):
			# TODO : 해당 헤더에 대한 지원 처리, headers 안에 해당 헤더가 없으면 BadRequest 를 리턴해야함
			pass
		return response
