# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI import (
	RequestProperties,
	Request,
)
from Liquirizia.WSGI.Validator import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *

from Liquirizia.Validator.Patterns import *

__all__ = (
	'RunPost'
)


@RequestProperties(
	method='POST',
	url='/api/content/array',
	body=Body(
		content=IsArray(
			error=BadRequestError('잘못된 배열 이어야 합니다.'),
		),
		formats={
			'application/json': JavaScriptObjectNotationDecoder(),
			'text/plain': TextEvaluateDecoder(),
		},
	),
	summary='컨텐츠 검증 샘플 - 배열',
	description='컨텐츠 검증 샘플 - 배열',
	tags='RequestRunner - Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, *content):
		return ResponseJSON({
			'content': content
		})
