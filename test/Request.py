# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Test import TestRequest

from Liquirizia.WSGI import Application
from Liquirizia.WSGI import Request, Response
from Liquirizia.WSGI.Properties import RequestRunner, RequestProperties
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Encoders import JavaScriptObjectNotationEncoder
from Liquirizia.WSGI.Validators import Body
from Liquirizia.WSGI.ContentReaders import JavaScriptObjectNotationContentReader
from Liquirizia.Validator.Patterns import *

from dataclasses import asdict
from json import loads


@RequestProperties(
	method='TEST',
	url='/:a/:b',
	body=Body(
		reader=JavaScriptObjectNotationContentReader(),
		content=IsObject(),
	)
)
class RunDelete(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self, **kwargs) -> Response:
		return ResponseJSON({
			'parameters': self.request.parameters,
			'headers': self.request.headers(),
			'qs': asdict(self.request.qs),
			'body': kwargs,
		})


class Request(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application())
		response = _.request(
			method='OPTIONS',
			uri='*'
		)
		ASSERT_TRUE(response.status in (200, 204))
		ASSERT_TRUE('TEST' in response.header('Allow'))
		response = _.request(
			method='OPTIONS',
			uri='/1/2'
		)
		ASSERT_TRUE(response.status in (200, 204))
		ASSERT_TRUE('TEST' in response.header('Allow'))
		ASSERT_TRUE('TEST' in response.header('Access-Control-Allow-Methods'))
		return

	@Order(1)	
	def testNotFound(self):
		_ = TestRequest(Application())
		response = _.request(
			method='TEST',
			uri='/'
		)
		ASSERT_IS_EQUAL(response.status, 404)
		return

	@Parameterized(
			{'qs': {'a': '1', 'b': '3'}, 'body': {'a': 1, 'b': 2, 'c': 3}},
	)
	@Order(2)
	def testRequest(self, qs, body):
		_ = TestRequest(Application())
		encode = JavaScriptObjectNotationEncoder('utf-8')
		response = _.request(
			method='TEST',
			uri='/1/2',
			qs=qs,
			body=encode(body),
			format='application/json',
			charset='utf-8',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		o = loads(response.body.decode(response.header('Content-Type').charset))
		ASSERT_IS_EQUAL(o['qs'], qs)
		ASSERT_IS_EQUAL(o['body'], body)
		return
