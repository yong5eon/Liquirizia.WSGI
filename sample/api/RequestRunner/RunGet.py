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
)
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import BadRequestError

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunGet'
)


@RequestProperties(
	method='GET',
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
	summary='Sample of GET',
	description='Sample of GET',
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
