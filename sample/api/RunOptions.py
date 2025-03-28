# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestProperties,
	RequestRunner,
	QueryString,
)
from Liquirizia.WSGI.Description import *
from Liquirizia.WSGI import Request, CORS, Router
from Liquirizia.WSGI.Errors import BadRequestError
from Liquirizia.WSGI.Responses import *

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunGet'
)


@RequestDescription(
	summary='OPTIONS 동작 샘플',
	description='OPTIONS 동작 샘플',
	tags='RequestRunner',
	qs={
		'p': String('경로'),
	},
	responses=(
		Response(
			status=200,
			description='완료',
			content=Content(
				format='application/json',
				schema=Object(
					properties=ObjectProperties(
						openapi=String('OAS(OpenAPI Specification) 버전', format='0.0.0'),
						info=Object(
							properties=ObjectProperties(
								title=String('제목'),
								version=String('버전', format='0.0.0'),
								summary=String('요약', required=False),
								description=String('설명', required=False),
								contact=Object(
									properties=ObjectProperties(
										name=String('이름'),
										url=String('URL', required=False),
										email=String('이메일', required=False),
									),
									requires=('name',),
								),
							),
							requires=('title', 'version'),
						),
						component=Object(),
						paths=Object(),
					),
				)
			),
		),
		Response(
			status=204,
			description='데이터 없음',
		),
		Response(
			status=400,
			description='잘못된 요청',
		)
	),
)
@RequestProperties(
	method='GET',
	url='/api/options',
	cors=CORS(),
	qs=QueryString(
		{
			'p': IsString(error=BadRequestError('경로(p) 는 문자열을 필요로 합니다')),
		},
		requires=('p',),
		requiresError=BadRequestError('질의에 경로(p) 는 필수 입니다.'),
		error=BadRequestError('질의를 필요로 합니다.')
	),
)
class RunOptions(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		router = Router()
		if self.request.qs.p == '*': 
			return ResponseNoContent(headers={
				'Allow': ', '.join(sorted(list(set(router.methods))))
			})
		url, patterns = router.matches(self.request.qs.p)
		if not patterns:
			raise BadRequestError('{} is not found in router'.format(self.request.qs.p))
		descriptor = Descriptor()
		doc = descriptor.toDocument(
			path=url,
			method=lambda m: {
				'POST': 1,
				'GET': 2,
				'PUT': 3,
				'DELETE': 4,
			}.get(m.upper(), 9),
		)
		if doc:
			response = ResponseJSON(doc, headers={
				'Allow': ', '.join(patterns.keys()),
				'Access-Control-Allow-Methods': ', '.join(patterns.keys()),
			})
		else:
			response = ResponseNoContent(headers={
				'Allow': ', '.join(patterns.keys()),
				'Access-Control-Allow-Methods': ', '.join(patterns.keys()),
			})
		cors = CORS()
		for _, match in patterns.items():
			if match.route.cors.origin: cors.origin.extend(match.route.cors.origin)
			if match.route.cors.headers: cors.headers.extend(match.route.cors.headers)
			if match.route.cors.credentials: cors.credentials = match.route.cors.credentials
			if match.route.cors.exposeHeaders: cors.exposeHeaders.extend(match.route.cors.exposeHeaders)
			if match.route.cors.age and match.route.cors.age > cors.age: cors.age = match.route.cors.age
		for k, v in cors.toHeaders().items(): response.header(k, v)
		return response
