# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import *
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
		reader=JavaScriptObjectNotationContentReader(),
		content=IsString(),
		type='application/json',
		format=String(),
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=String()
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
