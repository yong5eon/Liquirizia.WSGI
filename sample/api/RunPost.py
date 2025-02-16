# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestProperties, RequestRunner
from Liquirizia.WSGI import Request
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import BadRequestError
from Liquirizia.WSGI.Description import *

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestDescription(
	summary='POST 동작 샘플 ',
	description='POST 동작 샘플',
	tags='RequestRunner',
	responses=(
		Response(
			status=200,
			description='완료',
			content=Content(
				format='application/json',
				schema=Object(
					properties=ObjectProperties(
						status=Integer(description='상태'),
						message=String(description='메세지'),
						data=Object(
							properties=ObjectProperties(
								message=String(description='응답 스트링 에코'),
								res=Number(description='실행 결과'),
							),
							description='데이터',
						)
					),
					description='응답',
				),
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
				schema=Object(
					properties=ObjectProperties(
						reason=String(description='원인'),
						trace=String(description='오류 발생 장소'),
					)
				),
				example={
					'reason': '원인',
					'trace': '트래이스',
				},
			)
		)
	),
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
				schema=Object(
					properties=ObjectProperties(
						a=Integer(description='함수의 3차원 상수 a'),
						b=Number(description='함수의 3차원 상수 b'),
					)
				),
				example={
					'a': 0,
					'b': 0,
				},
			),
			Content(
				format='application/x-www-form',
				schema=Object(
					properties=ObjectProperties(
						a=Integer(description='함수의 3차원 상수 a'),
						b=Number(description='함수의 3차원 상수 b'),
					)
				),
				example='a=0&b=0',
			),
		),
		description='요청 본문'
	),
)
@RequestProperties(
	method='POST',
	url='/api/run/:a/:b',
	parameter=Validator(
		IsDictionary(
			IsRequiredIn('a', 'b', error=BadRequestError('경로에 a 와 b 는 필수 입니다.')),
			IsMappingOf({
				'a': Validator(
					IsNotToNone(error=BadRequestError('경로의 a 는 값이 있어야 합니다.')),
					ToInteger(error=BadRequestError('경로의 a는 정수를 필요로 합니다')),
					IsInteger(
						IsGreaterThan(100, error=BadRequestError('경로의 a 는 100 보다 커야 합니다')),
						error=BadRequestError('경로 a 는 정수를 필요로 합니다.')
					)
				),
				'b': Validator(
					IsNotToNone(error=BadRequestError('경로 b 는 값이 있어야 합니다')),
					ToInteger(error=BadRequestError('경로 b는 정수 필요로 합니다')),
					IsInteger(
						IsGreaterThan(100, error=BadRequestError('경로 b 는 100 보다 커야 합니다')),
						error=BadRequestError('경로 b는 정수 필요로 합니다')
					)
				),
			})
		)
	),
	qs=Validator(
		IsDictionary(
			IsRequiredIn('a', 'b', error=BadRequestError('질의에 a 와 b 는 필수 입니다.')),
			IsMappingOf({
				'a': Validator(
					IsNotToNone(error=BadRequestError('a 는 값이 있어야 합니다.')),
					ToInteger(error=BadRequestError('a는 정수를 필요로 합니다')),
					IsInteger(
						IsGreaterThan(5, error=BadRequestError('a 는 5보다 커야 합니다')),
						error=BadRequestError('a 는 정수를 필요로 합니다.')
					)
				),
				'b': Validator(
					IsNotToNone(error=BadRequestError('b 는 값이 있어야 합니다')),
					ToFloat(error=BadRequestError('b는 실수(부동 소수점)을 필요로 합니다')),
					IsFloat(
						IsGreaterThan(9, error=BadRequestError('b 는 9보다 커야 합니다')),
						error=BadRequestError('b 는 실수(부동 소수점)을 필요로 합니다.')
					)
				),
				'c': Validator(
					SetDefault(''),
					IsString(error=BadRequestError('c 는 문자열을 필요로 합니다.'))
				),
			})
		),
	),
	body=Validator(
		IsNotToNone(error=BadRequestError('본문에는 값이 있어야 합니다.')),
		IsDictionary(
			IsRequiredIn('a', 'b', error=BadRequestError('본문에 a 와 b 가 필요합니다')),
			IsMappingOf({
				'a': Validator(
					IsNotToNone(error=BadRequestError('a 는 값이 있어야 합니다.')),
					ToInteger(error=BadRequestError('a는 정수를 필요로 합니다')),
					IsInteger(
						IsLessThan(5, error=BadRequestError('a 는 5보다 작아야 합니다')),
						error=BadRequestError('a 는 정수를 필요로 합니다.')
					)
				),
				'b': Validator(
					IsNotToNone(error=BadRequestError('b 는 값이 있어야 합니다')),
					ToFloat(error=BadRequestError('b는 실수(부동 소수점)을 필요로 합니다')),
					IsFloat(
						IsLessThan(9, error=BadRequestError('b 는 9보다 작아야 합니다')),
						error=BadRequestError('b 는 실수(부동 소수점)을 필요로 합니다.')
					)
				),
			}),
		),
	),
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseJSON({
			'status': 200,
			'message': 'OK',
			'data': {
				'message': self.request.qs['c'],
				'res': self.request.parameters['a'] * self.request.qs['a'] + self.request.parameters['b'] * self.request.qs['b'] + self.request.body['a'] * self.request.body['b']
			},
		},
		headers={
			'X-Refresh-Token': self.request.header('X-Token')
		})
