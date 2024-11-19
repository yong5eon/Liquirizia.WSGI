# -*- coding: utf-8 -*-

from Liquirizia.WSGI import Request, RequestProperties
from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import BadRequestError
from Liquirizia.WSGI.Description import *

from Liquirizia.Validator import Validator
from Liquirizia.Validator.Patterns import *


__all__ = (
	'RunGet'
)

@RequestProperties(
	method='GET',
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
	header=Validator(
		IsDictionary(
			IsRequiredIn('X-Token', error=BadRequestError('헤더에 토큰(X-Token)이 필요합니다'))
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
						error=BadRequestError('c는 정수를 필요로 합니다.')
					)
				),
				'b': Validator(
					IsNotToNone(error=BadRequestError('b 는 값이 있어야 합니다')),
					ToFloat(error=BadRequestError('b는 실수(부동 소수점)을 필요로 합니다')),
					IsFloat(
						IsGreaterThan(9, error=BadRequestError('b 는 9보다 커야 합니다')),
						error=BadRequestError('b는 실수(부동 소수점)을 필요로 합니다')
					)
				),
				'c': Validator(
					SetDefault(''),
					IsString(error=BadRequestError('c는 문자열을 필요로 합니다'))
				),
			})
		),
	),
	description=Description(
		description='GET 동작 샘플',
		summary='GET 을 동작 샘플 ',
		tags='RequestRunner',
		responses=(
			DescriptionResponse(
				status=200,
				description='완료',
				body=DescriptionResponseBody(
					format='application/json',
					content=Object(
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
				headers=DescriptionResponseHeader(
					name='X-Refresh-Token',
					description='리프레시 토큰',
					type=PropertyType.String,
				)
			),
			DescriptionResponse(
				status=400,
				description='잘못된 요청',
				body=DescriptionResponseBody(
					format='application/json',
					content=Object(
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
		parameter=(
			DescriptionRequestParameter(
				name='a',
				description='동작의 상수 a 값, a 는 100 보다 커야함',
				type=PropertyType.Integer,
				min=100,
				required=True,
			),
			DescriptionRequestParameter(
				name='b',
				description='동작의 상수 b 값, b 는 100 보다 커야함',
				min=100,
				type=PropertyType.Number,
				required=True,
			),
		),
		header=(
			DescriptionRequestHeader(
				name='X-Token',
				description='인증을 위한 토큰',
				type=PropertyType.String,
				required=True,
			),
		),
		qs=(
			DescriptionRequestQueryString(
				name='a',
				description='동작의 상수 a 값, a 는 5 보다 커야함',
				type=PropertyType.Integer,
				min=5,
				required=True,
			),
			DescriptionRequestQueryString(
				name='b',
				description='동작의 상수 b 값, b 는 10 보다 커야함',
				type=PropertyType.Number,
				min=10,
				required=True,
			),
			DescriptionRequestQueryString(
				name='c',
				description='동작의 상수 c 값',
				type=PropertyType.String,
				default='',
				required=False,
			)
		),
	),
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
				'message': self.request.qs['c'],
				'res': self.request.parameters['a'] * self.request.qs['a'] + self.request.parameters['b'] * self.request.qs['b'] 
			},
		},
		headers={
			'X-Refresh-Token': self.request.header('X-Token')
		})
