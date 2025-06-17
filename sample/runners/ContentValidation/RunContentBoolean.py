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
	url='/api/content/bool',
	body=Body(
		reader=JavaScriptObjectNotationContentReader(
			va=IsBoolean(),
		),
		content=Content(
			format='application/json',
			schema=Boolean()
		)
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=Boolean()
		)
	),
	summary='컨텐츠 검증 샘플 - 불리언',
	description='컨텐츠 검증 샘플 - 불리언',
	tags='Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, content: bool):
		return ResponseJSON(content)
