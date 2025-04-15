# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Authorizations import HTTP
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
	auth=HTTP(
		scheme='Bearer',
		format='JWT',
		auth=GetSession(),
		errorParameters={
			'realm': 'Liquirizia.WSGI',
			'tokenUrl': '/api/auth/token/refresh',
			'refreshUrl': '/api/auth/token/refresh',
		}
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
