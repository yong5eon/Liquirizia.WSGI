# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI import RequestProperties
from Liquirizia.WSGI.Validator import QueryString
from Liquirizia.WSGI import Request, Router
from Liquirizia.WSGI.Errors import BadRequestError
from Liquirizia.WSGI.Responses import *

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunGet'
)


@RequestProperties(
	method='GET',
	url='/api/options',
	qs=QueryString(
		{
			'p': IsString(error=BadRequestError('경로(p) 는 문자열을 필요로 합니다')),
		},
		requires=('p',),
		requiresError=BadRequestError('질의에 경로(p) 는 필수 입니다.'),
		error=BadRequestError('질의를 필요로 합니다.')
	),
)
class RunOptions(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		# TODO : implement OPTIONS
		return ResponseOK()
