# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request

from Liquirizia.Validator.Patterns import *
from Liquirizia.Validator.Patterns.Object import *

__all__ = (
	'RunPut'
)


@RequestProperties(
	method='PUT',
	url='/api/run/:a/:b',
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
	),
	header=Header(
		{
			'X-Token': IsString(
				error=BadRequestError('헤더 X-Token 은 문자열을 필요로 합니다'),
			),
		},
		requires=('X-Token',),
		requiresError=BadRequestError('헤더 X-Token 은 필수 입니다.'),
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
		formats={
			'application/json': JavaScriptObjectNotationDecoder(error=BadRequestError('올바르지 않은 JSON 형식입니다.')),
			'application/x-www-form-urlencoded': FormUrlEncodedDecoder(error=BadRequestError('올바르지 않은 FormUrlEncoded 형식입니다.')),
		},
		error=BadRequestError('알 수 없는 형식입니다.'),
		unsupportedError=UnsupportedMediaTypeError('지원하지 않는 미디어 타입입니다.')
	),
	summary='Sample of PUT',
	description='Sample of PUT',
	tags='RequestRunner',
)
class RunPut(RequestRunner):
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
				'ret': (self.request.parameters.a + self.request.qs.b * a) * (self.request.parameters.b + self.request.qs.b * b), 
			},
		},
		headers={
			'X-Refresh-Token': self.request.header('X-Token')
		})
