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
from Liquirizia.Validator.Patterns.Object import *
from Liquirizia.Description import *

from ..Session import GetSession
from ..Model import *

__all__ = (
	'RunDelete'
)


@RequestProperties(
	method='DELETE',
	url='/api/run/:a/:b',
	origin=Origin(('http://localhost')),
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
	body=Body(
		IsObject(
			IsRequiredIn('a', 'b', error=BadRequestError('본문에는 a 와 b 값이 있어야 합니다.')),
			IsMappingOf(
				{
					'a': ToInteger(
						IsLessThan(5, error=BadRequestError('본문 a 는 5보다 작아야 합니다.')),
						error=BadRequestError('본문 a는 정수를 필요로 합니다'),
					),
					'b': ToNumber(
						IsLessThan(9, error=BadRequestError('본문 b 는 9보다 작아야 합니다.')),
						error=BadRequestError('본문 b는 실수를 필요로 합니다.'),
					),
				},
			),
			error=BadRequestError('본문은 오브젝트 형식의 값을 필요로 합니다.'),
		),
		decoders={
			'application/json': JavaScriptObjectNotationDecoder(error=BadRequestError('올바르지 않은 JSON 형식입니다.')),
			'application/x-www-form-urlencoded': FormUrlEncodedDecoder(error=BadRequestError('올바르지 않은 FormUrlEncoded 형식입니다.')),
		},
		error=BadRequestError('알 수 없는 형식입니다.'),
		unsupportedError=UnsupportedMediaTypeError('지원하지 않는 미디어 타입입니다.'),
		format=Object(
			properties=Properties(
				a=Integer('본문 a', max=5),
				b=Number('본문 b', max=9),
			)
		)
	),
	response=(
		Response(
			status=200,
			description='성공',
			content=Content(
				format='application/json',
				schema=ToSchema(ResponseModel)
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
		Response(
			status=403,
			description='권한없음',
			content=Content(
				format='text/plain',
				schema=String('원인'),
			),
		),
	),
	summary='DELETE 요청을 처리하는 예제',
	tags='RequestRunner',
)
class RunDelete(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, a: int, b: float):
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
					'content': {
						'a': a,
						'b': b,
					}
				},
				'ret': (self.request.parameters.a + self.request.qs.b - a) * (self.request.parameters.b + self.request.qs.b - b), 
			},
		},
		headers={
			'X-Refresh-Token': self.request.header('X-Token')
		})
