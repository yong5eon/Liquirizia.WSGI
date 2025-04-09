# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Properties.Validator import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunGet'
)


@RequestProperties(
	method='GET',
	url='/options',
	qs=QueryString(
		{
			'p': IsString(error=BadRequestError('경로(p) 는 문자열을 필요로 합니다')),
		},
		requires=('p',),
		requiresError=BadRequestError('질의에 경로(p) 는 필수 입니다.'),
	),
	tags='ETC',
)
class RunOptions(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		# TODO : implement OPTIONS
		return ResponseOK()
