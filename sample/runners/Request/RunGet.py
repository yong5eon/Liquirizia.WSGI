# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Properties.Validator import *
from Liquirizia.WSGI.Properties.Auth import HTTP as HTTPAuthenticate
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import	Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

from ..Session import GetSession
from ..Model import *

__all__ = (
	'RunGet'
)


@RequestProperties(
	method='GET',
	url='/api/run/:a/:b',
	origin=Origin(all=True),
	auth=HTTPAuthenticate(
		scheme='Bearer',
		format='JWT',
		optional=True,
		auth=GetSession(),
		schemeError=UnauthorizedError('스키마가 올바르지 않습니다,'),
		schemeErrorParameters={
			'realm': '로그인',
		},
		error=UnauthorizedError('인증이 필요합니다.'),
	),
	parameter=Parameter(
		{
			'a': ToInteger(
				IsGreaterThan(100, error=BadRequestError('파라미터 a 는 100 보다 커야 합니다.')),
				error=BadRequestError('파라미터 a 는 정수를 필요로 합니다.'),
			), 
			'b': ToInteger(
				IsGreaterThan(100, error=BadRequestError('파라미터 b 는 100 보다 커야 합니다.')),
				error=BadRequestError('파라미터 b 는 정수를 필요로 합니다.'),
			),
		},
		format={
			'a': Integer('파라미터 a', min=100),
			'b': Integer('파라미터 b', min=100),
		}
	),
	qs=QueryString(
		{
			'a': ToInteger(
				IsGreaterThan(5, error=BadRequestError('질의 a 는 5보다 커야 합니다.')),
				error=BadRequestError('질의 a 는 정수를 필요로 합니다.'),
			),
			'b': ToNumber(
				IsGreaterThan(9, error=BadRequestError('질의 b 는 9보다 커야 합니다.')),
				error=BadRequestError('질의 b 는 실수여야 합니다.'),
			),
			'c': (
				SetDefault('안녕'),
				IsString(error=BadRequestError('질의 c 는 문자열을 필요로 합니다')),
			),
		},
		requires=('a', 'b'),
		requiresError=BadRequestError('질의 a 와 b 는 필수 입니다.'),
		format={
			'a': Integer('질의 a', min=5),
			'b': Number('질의 b', min=9),
			'c': String('질의 c', default='안녕', required=False),
		}
	),
	header=Header(
		{
			'X-App-Id': IsToNone(IsString()),
		},
		format={
			'X-App-Id': String(required=False),
		},
	),
	response=(
		Response(
			status=200,
			description='성공',
			content=Content(
				format='application/json',
				schema=Object(
					properties=Properties(
						status=Integer('상태코드'),
						message=String('메세지'),
						data=FORMAT_DATA,
					)
				)
			),
		),
		Response(
			status=400,
			description='잘못된 요청',
			content=Content(
				format='text/plain',
				schema=String('원인'),
			),
		),
	),
	summary='GET 요청을 처리하는 예제',
	tags='RequestRunner',
)
class RunGet(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseJSON({
			'status': 200,
			'message': 'OK',
			'data': {
				'message': self.request.qs.c,
				'args': {
					'parameters': {
						'a': self.request.parameters.a,
						'b': self.request.parameters.b,
					},
					'qs': {
						'a': self.request.qs.a,
						'b': self.request.qs.b,
					},
				},
				'ret': (self.request.parameters.a + self.request.qs.b) * (self.request.parameters.b + self.request.qs.b),
			},
		},
		headers={
			'X-Refresh-Token': self.request.header('X-Token')
		})
