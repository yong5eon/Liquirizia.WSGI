# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Validator.Patterns.Object import *
from Liquirizia.Description import *

__all__ = (
	'RunAuthOAuth2ImplicitToken',
)


@RequestProperties(
	method='GET',
	url='/api/auth/oauth2/implicit/token',
	qs=QueryString(
		{
			'response_type': IsString(IsIn('token')),
			'client_id': IsString(),
			'redirect_uri': IsToNone(IsString()),
			'state': IsToNone(IsString()),
		},
		requires=('response_type', 'client_id'),
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
	summary='OAuth2Implicit 접큰키를 얻기위한 예제',
	tags='Auth',
)
class RunAuthOAuth2ImplicitTOken(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		from random import randint
		return ResponseJSON({
			'access_token': str(1),
			'refresh_token': str(1),
		})
