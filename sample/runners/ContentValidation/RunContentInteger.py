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
	url='/api/content/integer',
	body=Body(
		reader=JavaScriptObjectNotationContentReader(),
		content=IsInteger(),
		type='application/json',
		format=Integer(),
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=Integer()
		)
	),
	summary='컨텐츠 검증 샘플 - 정수',
	description='컨텐츠 검증 샘플 - 정수',
	tags='Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, content: int):
		return ResponseJSON(content)
