# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Properties.Validator import *
from Liquirizia.WSGI.Properties.Auth import HTTP as HTTPAuthenticate
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

from ..Session import GetSession
from dataclasses import asdict

__all__ = (
	'RunAuthHTTP'
)


@RequestProperties(
	method='GET',
	url='/api/auth/http',
	auth=HTTPAuthenticate(
		scheme='Bearer',
		format='JWT',
		auth=GetSession(),
		schemeError=UnauthorizedError('스키마가 올바르지 않습니다,'),
		schemeErrorParameters={
			'realm': '로그인',
		},
		error=UnauthorizedError('인증이 필요합니다.'),
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=Object( # TODO: make Schema from Session dataclass
				properties=Properties(
					credentials=String(),
					extra=Object(),
				)
			)
		)
	),
	summary='HTTP 인증이 필요한 요청을 처리하는 예제',
	tags='Auth',
)
class RunAuthHTTP(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseJSON(asdict(self.request.session) if self.request.session else {})
