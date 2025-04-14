# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Validators import *
from Liquirizia.WSGI.ContentReaders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Validator.Patterns.Object import *
from Liquirizia.Description import *

__all__ = (
	'RunAuthToken',
)


@RequestProperties(
	method='POST',
	url='/api/auth/token',
	body=Body(
		type='application/x-www-form-urlencoded',
		reader=FormUrlEncodedContentReader(),
		content=IsObject(
			IsRequiredIn('username', 'password'),
			IsMappingOf({
				'username': IsString(),
				'password': IsString(),
				'client_id': IsToNone(IsString()),
				'client_secret': IsToNone(IsString()),
				'grant_type': (
					SetDefault('password'),
					IsString(IsIn('password')),
				),
			}),
		),
		format=Object(
			properties=Properties(
				username=String(
					description='사용자 이름',
					required=True,
				),
				password=String(
					description='비밀번호',
					required=True,
				),
				client_id=String(
					description='클라이언트 아이디',
					required=False,
				),
				client_secret=String(
					description='클라이언트 비밀번호',
					required=False,
				),
				grant_type=String(
					description='인증 방식',
					enum=['password'],
					required=False,
				),
			),
		)
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
	summary='OAuth2 접큰키를 얻기위한 예제',
	tags='Auth',
)
class RunAuthToken(RequestRunner):
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
			# 'access_token': str(randint(0, 1)),
			'access_token': '1',
			# 'refresh_token': str(randint(0, 1)),
			'refresh_token': '1',
		})
