# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Properties.Validator import *
from Liquirizia.WSGI.Properties.Auth import Header as HeaderAuthenticate
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
	'RunAuthHeader',
)


@RequestProperties(
	method='GET',
	url='/api/auth/header',
	auth=HeaderAuthenticate(
		name='Credentials',
		auth=GetSession(),
		error=UnauthorizedError('인증이 필요합니다.'),
	),
	response=(
		Response(
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
		Response(
			status=401,
			description='인증 실패',
			content=Content(
				format='text/plain',
				schema=String('원인')
			)
		)
	),
	summary='헤더 인증이 필요한 요청을 처리하는 예제',
	tags='Auth',
)
class RunAuthHeader(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseJSON(asdict(self.request.session) if self.request.session else {})
