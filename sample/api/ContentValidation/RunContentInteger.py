# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI import RequestProperties, Request
from Liquirizia.WSGI.Validator import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import BadRequestError

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestProperties(
	method='POST',
	url='/api/content/integer',
	body=Body(
		content=IsInteger(error=BadRequestError('본문은 정수를 필요로 합니다.')),
		formats={
			'application/json': JavaScriptObjectNotationDecoder(),
			'text/plain': TextEvaluateDecoder(),
		},
	),
	summary='컨텐츠 검증 샘플 - 정수',
	description='컨텐츠 검증 샘플 - 정수',
	tags='RequestRunner - Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, content: bool):
		return ResponseJSON({
			'content': content
		})
