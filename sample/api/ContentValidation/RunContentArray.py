# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI import (
	Request,
	RequestProperties,
)
from Liquirizia.WSGI.Validator import *
from Liquirizia.WSGI.Validators import *
from Liquirizia.WSGI.Decoders import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *

__all__ = (
	'RunPost'
)


@RequestProperties(
	method='POST',
	url='/api/content/array',
	body=Body(
		content=Content(
			decode=JavaScriptObjectNotationDecoder(),
			va=ToArray(error=BadRequestError('잘못된 본문 정보 입니다.')),
		),
		description='컨텐츠 검증 샘플 - 배열',
		required=True,
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
