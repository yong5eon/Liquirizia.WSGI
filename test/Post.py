# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.WSGI import (
		Application, 
		Configuration,
		CORS,
)

from Liquirizia.WSGI import Request, Response
from Liquirizia.WSGI.Properties import RequestRunner, RequestProperties
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Encoders import JavaScriptObjectNotationEncoder

from Liquirizia.WSGI.Test import TestRequest

from dataclasses import asdict


@RequestProperties(
	method='POST',
	url='/',
	cors=CORS(
		headers=['Content-Type', 'Content-Length']
	)
)
class RunPost(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self, **kwargs) -> Response:
		return ResponseJSON({
			'qs': asdict(self.request.qs),
			'body': kwargs,
		})


class TestPost(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='OPTIONS',
			uri='*'
		)
		ASSERT_TRUE(response.status in (200, 204))
		ASSERT_IS_EQUAL('POST' in response.header('Allow'), True)
		response = _.request(
			method='OPTIONS',
			uri='/'
		)
		ASSERT_TRUE(response.status in (200, 204))
		ASSERT_IS_EQUAL('POST' in response.header('Allow'), True)
		ASSERT_IS_EQUAL('POST' in response.header('Access-Control-Allow-Methods'), True)
		headers = response.header('Access-Control-Allow-Headers')
		others = ['Content-Type', 'Content-Length']
		for other in others:
			ASSERT_IS_EQUAL(other in headers, True)
		return

	@Parameterized(
			{'qs': {'a': '1', 'b': '3'}, 'body': {'a': 1, 'b': 2, 'c': 3}},
	)
	@Order(1)
	def testRequest(self, qs, body):
		_ = TestRequest(Application(conf=Configuration()))
		encode = JavaScriptObjectNotationEncoder('utf-8')
		response = _.request(
			method='POST',
			uri='/',
			qs=qs,
			body=encode(body),
			format='application/json',
			charset='utf-8',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		headers = response.header('Access-Control-Allow-Headers')
		others = ['Content-Type', 'Content-Length']
		for other in others:
			ASSERT_IS_EQUAL(other in headers, True)
		ASSERT_IS_EQUAL(response.body['qs'], qs)
		ASSERT_IS_EQUAL(response.body['body'], body)
		return
