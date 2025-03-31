# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import (
	RequestProperties,
	RequestRunner,
)
from Liquirizia.WSGI.Description import *
from Liquirizia.WSGI import Request, CORS
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import BadRequestError

from .Format import *

__all__ = (
	'RunStatus'
)


@RequestDescription(
	summary='상태 확인',
	description='상태 확인',
	tags='RequestRunner',
	responses=(
		Response(
			status=200,
			description='완료',
		),
		Response(
			status=400,
			description='잘못된 요청',
			content=Content(
				format='application/json',
				schema=FormatError,
			)
		)
	),
)
@RequestProperties(
	method='GET',
	url='/',
	cors=CORS(),
)
class RunGet(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseOK()
