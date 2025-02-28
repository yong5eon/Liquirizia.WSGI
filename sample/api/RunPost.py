# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestProperties,
	Parameter as ParameterValidator,
	QueryString as QueryStringValidator,
	Header as HeaderValidator,
	Object as ObjectValidator,
	RequestRunner,
)
from Liquirizia.WSGI import Request, CORS
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import BadRequestError
from Liquirizia.WSGI.Description import (
	RequestDescription,
	Body,
	Response,
	Content,
	Object,
	ObjectProperties,
	String,
	Number,
	Integer,
)

from Liquirizia.Validator.Patterns import *

from .Format import *

__all__ = (
	'RunPost'
)


@RequestDescription(
	summary='POST 동작 샘플',
	description='POST 동작 샘플',
	tags='RequestRunner',
	parameters={
		'a': Integer(
			description='동작의 상수 a 값, a 는 100 보다 커야함',
			min=100,
			required=True,
		),
		'b': Number(
			description='동작의 상수 b 값, b 는 100 보다 커야함',
			min=100,
			required=True,
		),
	},
	headers={
		'X-Token': String(
			description='인증을 위한 토큰',
			required=True,
		),
	},
	qs={
		'a': Integer(
			description='동작의 상수 a 값, a 는 5 보다 커야함',
			min=5,
			required=True,
		),
		'b': Number(
			description='동작의 상수 b 값, b 는 10 보다 커야함',
			min=10,
			required=True,
		),
		'c': String(
			description='동작의 상수 c 값',
			default='',
			required=False,
		)
	},
	body=Body(
		content=(
			Content(
				format='application/json',
				schema=FormatRequest(),
				example={
					'a': 0,
					'b': 0,
				},
			),
			Content(
				format='application/x-www-form',
				schema=FormatRequest(),
				example='a=0&b=0',
			),
		),
	),
	responses=(
		Response(
			status=200,
			description='완료',
			content=Content(
				format='application/json',
				schema=FormatResponse(),
				example={
					'status': 200,
					'message': 'OK',
					'data': {
						'message': 'message',
						'res': 0.0,
					},
				}
			),
			headers={
				'X-Refresh-Token': String(description='리프레시 토큰')
			}
		),
		Response(
			status=400,
			description='잘못된 요청',
			content=Content(
				format='application/json',
				schema=FormatError(),
				example={
					'reason': '원인',
					'trace': '트래이스',
				},
			)
		)
	),
	order=1,
)
@RequestProperties(
	method='POST',
	url='/api/run/:a/:b',
	cors=CORS(
		headers=['X-Token'],
		exposeHeaders=['X-Refresh-Token'],
	),
	parameter=ParameterValidator({
		'a': (
			ToInteger(error=BadRequestError('경로 a 는 정수를 필요로 합니다.')), 
			IsInteger(
				IsGreaterThan(100, error=BadRequestError('경로의 a 는 100 보다 커야 합니다')),
				error=BadRequestError('경로 a 는 정수를 필요로 합니다.')
			),
		),
		'b': (
			ToInteger(error=BadRequestError('경로 b는 정수 필요로 합니다')),
			IsInteger(
				IsGreaterThan(100, error=BadRequestError('경로 b 는 100 보다 커야 합니다')),
				error=BadRequestError('경로 b는 정수 필요로 합니다')
			),
		),
	}),
	header=HeaderValidator(
		requires=('X-Token',),
		requiresError=BadRequestError('헤더에 X-Token 값을 필요로 합니다.'),
	),
	qs=QueryStringValidator(
		mappings={
			'a': (
				ToInteger(error=BadRequestError('a는 정수를 필요로 합니다')),
				IsInteger(
					IsGreaterThan(5, error=BadRequestError('a 는 5보다 커야 합니다')),
					error=BadRequestError('c는 정수를 필요로 합니다.')
				),
			),
			'b': (
				ToFloat(error=BadRequestError('b 는 실수(부동 소수점)을 필요로 합니다')),
				IsFloat(
					IsGreaterThan(9, error=BadRequestError('b 는 9보다 커야 합니다')),
					error=BadRequestError('b는 실수(부동 소수점)을 필요로 합니다')
				),
			),
			'c': (
				SetDefault(''),
				IsString(error=BadRequestError('c는 문자열을 필요로 합니다'))
			),
		},
		requires=('a', 'b'),
		requiresError=BadRequestError('질의에 a 와 b 는 필수 입니다.'),
		error=BadRequestError('질의를 필요로 합니다.')
	),
	content=ObjectValidator(
		mappings={
			'a': (
				ToInteger(error=BadRequestError('a는 정수를 필요로 합니다')),
				IsInteger(
					IsLessThan(5, error=BadRequestError('a 는 5보다 작아야 합니다')),
					error=BadRequestError('a 는 정수를 필요로 합니다.')
				),
			),
			'b': (
				ToFloat(error=BadRequestError('b는 실수(부동 소수점)을 필요로 합니다')),
				IsFloat(
					IsLessThan(9, error=BadRequestError('b 는 9보다 작아야 합니다')),
					error=BadRequestError('b 는 실수(부동 소수점)을 필요로 합니다.')
				),
			),
		},
		requires=('a', 'b'),
		requiresError=BadRequestError('본문에는 a 와 b 값이 있어야 합니다.'),
		error=BadRequestError('본문에는 값이 있어야 합니다.')
	)
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, a: int, b: float):
		return ResponseJSON({
			'status': 200,
			'message': 'OK',
			'data': {
				'message': self.request.qs.c,
				'res': {
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
				}
			},
		},
		headers={
			'X-Refresh-Token': self.request.header('X-Token')
		})
