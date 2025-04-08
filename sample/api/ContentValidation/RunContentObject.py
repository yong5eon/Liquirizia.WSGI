# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestProperties(
	method='POST',
	url='/api/content/object',
	body=Body(
		content=IsObject(error=BadRequestError('본문은 오브젝트 형태여야 합니다.')),
		decoders={
			'application/json': JavaScriptObjectNotationDecoder(),
			'text/plain': TextEvaluateDecoder(),
		},
	),
	summary='컨텐츠 검증 샘플 - 객체',
	description='컨텐츠 검증 샘플 - 객체',
	tags='RequestRunner - Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, **content):
		return ResponseJSON({
			'content': content
		})
