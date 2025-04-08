# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request

from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

__all__ = (
	'RunGet'
)


class Auth(Authorization):
	def __call__(self, credentials: str):
		print(credentials)
		return True

@RequestProperties(
	method='GET',
	url='/api/run/auth/http',
	auth=HTTP(
		scheme='Bearer',
		auth=Auth(),
		schemeError=UnauthorizedError('스키마가 올바르지 않습니다,'),
		schemeErrorParameters={
			'realm': '로그인',
		}
	),
	summary='HTTP 인증이 필요한 요청을 처리하는 예제',
	tags='RequestRunner - Authorization',
)
class RunAuthHTTP(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseOK()
