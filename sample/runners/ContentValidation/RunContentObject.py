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
	url='/api/content/object',
	body=Body(
		reader=JavaScriptObjectNotationContentReader(),
		content=IsObject(),
		type='application/json',
		format=Object(),
	),
	response=Response(
		status=200,
		description='성공',
		content=Content(
			format='application/json',
			schema=Object()
		)
	),
	summary='컨텐츠 검증 샘플 - 객체',
	description='컨텐츠 검증 샘플 - 객체',
	tags='Content Validation',
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self, **content):
		return ResponseJSON(content)
