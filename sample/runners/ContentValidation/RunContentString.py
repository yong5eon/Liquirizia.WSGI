# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Properties.Validator import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import	Response, Content


from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

__all__ = (
	'RunPost'
)


@RequestProperties(
	method='POST',
	url='/api/content/string',
	body=Body(
		content=IsString(error=BadRequestError('본문은 문자열 이어야 합니다.')),
		decoders={
			'application/json': JavaScriptObjectNotationDecoder(),
			'text/plain': TextEvaluateDecoder(),
		},
		format=String(),
	),
	response=(
		Response(
			status=200,
			description='성공',
			content=Content(
				format='application/json',
				schema=String()
			)
		),
		Response(
			status=400,
			description='잘못된 요청',
			content=Content(
				format='text/plain',
				schema=String('원인')
			)
		)
	),
	summary='컨텐츠 검증 샘플 - 문자열',
	description='컨텐츠 검증 샘플 - 문자열',
	tags='Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, content: str):
		return ResponseJSON(content)
