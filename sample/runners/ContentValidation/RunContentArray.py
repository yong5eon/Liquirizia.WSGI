# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *
from Liquirizia.WSGI import	Request
from Liquirizia.WSGI.Description import Response, Content

from Liquirizia.Validator.Patterns import *
from Liquirizia.Description import *

__all__ = (
	'RunPost'
)


@RequestProperties(
	method='POST',
	url='/api/content/array',
	body=Body(
		reader=JavaScriptObjectNotationContentReader(),
		content=IsArray(),
		type='application/json',
		format=Array()
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=Array()
		)
	),
	summary='컨텐츠 검증 샘플 - 배열',
	description='컨텐츠 검증 샘플 - 배열',
	tags='Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, *content):
		return ResponseJSON(content)
