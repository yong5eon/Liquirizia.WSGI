# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI import (
	RequestProperties,
	Request,
)
from Liquirizia.WSGI.Validator import (
	Parameter,
	QueryString,
	Header,
	Body,
)
from Liquirizia.WSGI.Validators import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import (
	BadRequestError,
	UnsupportedMediaTypeError,
)

from Liquirizia.Validator.Patterns import (
	SetDefault,
	IsGreaterThan,
	IsLessThan,
)

__all__ = (
	'RunPost'
)


@RequestProperties(
	method='POST',
	url='/api/run/:a/:b',
	parameter=Parameter(
		{
			'a': ToInteger(
				IsGreaterThan(100, error=BadRequestError('경로의 a 는 100 보다 커야 합니다')),
				error=BadRequestError('경로 a 는 정수를 필요로 합니다.')
			), 
			'b': ToInteger(
				IsGreaterThan(100, error=BadRequestError('경로 b 는 100 보다 커야 합니다')),
				error=BadRequestError('경로 b는 정수 필요로 합니다')
			),
		}
	),
	qs=QueryString(
		{
			'a': ToInteger(
				IsGreaterThan(5, error=BadRequestError('a 는 5보다 커야 합니다')),
				error=BadRequestError('a 는 정수를 필요로 합니다')
			),
			'b': ToNumber(
				IsGreaterThan(9, error=BadRequestError('b 는 9보다 커야 합니다')),
				error=BadRequestError('b 는 실수(부동 소수점)을 필요로 합니다')
			),
			'c': (SetDefault(''), IsString(error=BadRequestError('c는 문자열을 필요로 합니다'))),
		},
		requires=('a', 'b'),
		requiresError=BadRequestError('질의에 a 와 b 는 필수 입니다.'),
	),
	header=Header(
		{
			'X-Token': IsString(error=BadRequestError('헤더 X-Token 은 문자열을 필요로 합니다')),
		},
		requires=('X-Token',),
		requiresError=BadRequestError('헤더에 X-Token 값을 필요로 합니다.'),
	),
	body=Body(
		IsObject(
			{
				'a': ToInteger(
					IsLessThan(5, error=BadRequestError('a 는 5보다 작아야 합니다')),
					error=BadRequestError('a는 정수를 필요로 합니다')
				),
				'b': ToNumber(
					IsLessThan(9, error=BadRequestError('b 는 9보다 작아야 합니다')),
					error=BadRequestError('b는 실수(부동 소수점)을 필요로 합니다')
				),
			},
			requires=('a', 'b'),
			requiresError=BadRequestError('본문에는 a 와 b 값이 있어야 합니다.'),
			requiredError=BadRequestError('본문에는 값이 있어야 합니다.'),
			error=BadRequestError('본문은 오브젝트 형식이어야 합니다'),
		),
		formats={
			'application/json': JavaScriptObjectNotationDecoder(error=BadRequestError('올바르지 않은 JSON 형식입니다.')),
			'application/x-www-form-urlencoded': FormUrlEncodedDecoder(error=BadRequestError('올바르지 않은 FormUrlEncoded 형식입니다.')),
		},
		error=UnsupportedMediaTypeError('지원하지 않는 미디어 타입입니다.')
	),
	summary='Sample of POST',
	description='Sample of POST',
	tags='RequestRunner',
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
