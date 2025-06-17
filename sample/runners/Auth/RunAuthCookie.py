# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import	Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

from dataclasses import dataclass


__all__ = (
	'RunAuthCookie'
)

@dataclass
class Session(object):
	credentials: str
	extra: dict = None


class GetSession(Authorization):
	def __call__(self, credentials: str):
		if credentials != '1':
			raise UnauthorizedError(reason='Invalid credentials')
		return Session(
			credentials=credentials,
			extra={
				'id': 0,
			},
		)


@RequestProperties(
	method='GET',
	url='/api/auth/cookie',
	auth=Auth(
		auth=GetSession(),
		credentials=Cookie(
			name='credentials',
		),
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
	summary='쿠기 인증이 필요한 요청을 처리하는 예제',
	tags='Auth',
)
class RunAuthCookie(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseJSON(self.request.session if self.request.session else {})
