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
	'RunAuthOAuth2PasswordToken',
)


@RequestProperties(
	method='POST',
	url='/api/auth/oauth2/password/token',
	body=Body(
		reader=FormUrlEncodedContentReader(
			va=IsObject(
				IsRequiredIn('username', 'password'),
				IsMappingOf({
					'username': IsString(),
					'password': IsString(),
					'client_id': Optional(IsString()),
					'client_secret': Optional(IsString()),
					'grant_type': (
						SetDefault('password'),
						IsString(IsIn('password')),
					),
				}),
			),
		),
		content=Content(
			format='application/x-www-form-urlencoded',
			schema=Object(
				properties=Properties(
					username=String('사용자 이름', required=True),
					password=String('비밀번호', required=True),
					client_id=String('클라이언트 아이디', required=False),
					client_secret=String('클라이언트 비밀번호', required=False),
					grant_type=String(
						description='인증 방식',
						enum=['password'],
						required=False,
					),
				),
			),
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
	summary='OAuth2Password 접큰키를 얻기위한 예제',
	tags='Auth',
)
class RunAuthOAuth2PasswordTOken(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(
		self,
		username: str,
		password: str,
		client_id: str = None,
		client_secret: str = None,
		grant_type: str = 'password',
	):
		from random import randint
		return ResponseJSON({
			'username': username,
			'password': password,
			'client_id': client_id,
			'client_secret': client_secret,
			'grant_type': grant_type,
			'access_token': str(1),
			'refresh_token': str(1),
		})
