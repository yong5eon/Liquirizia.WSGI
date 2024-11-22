# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.WSGI import (
		Application, 
		Configuration,
		CORS,
)

from Liquirizia.WSGI import Request, RequestProperties, Response
from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI.Responses import *

from Liquirizia.WSGI.Test import TestRequest

from Liquirizia.Serializer import SerializerHelper


@RequestProperties(
	method='DELETE',
	url='/',
	cors=CORS(
		headers=['Content-Type', 'Content-Length']
	)
)
class RunDelete(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self) -> Response:
		return ResponseJSON({
			'qs': self.request.qs,
			'body': self.request.body,
		})


class TestDelete(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='OPTIONS',
			uri='/'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_IS_EQUAL('DELETE' in response.header('Allow').split(', '), True)
		ASSERT_IS_EQUAL('DELETE' in response.header('Access-Control-Allow-Methods').split(', '), True)
		headers = response.header('Access-Control-Allow-Headers').split(', ').sort()
		others = 'Content-Type, Content-Length'.split(', ').sort()
		ASSERT_IS_EQUAL(headers, others)
		return

	@Parameterized(
			{'qs': {'a': '1', 'b': '3'}, 'body': {'a': 1, 'b': 2, 'c': 3}},
	)
	@Order(1)
	def testRequest(self, qs, body):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='DELETE',
			uri='/',
			qs=qs,
			body=SerializerHelper.Encode(body, 'application/json', 'utf-8'),
			format='application/json',
			charset='utf-8',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		headers = response.header('Access-Control-Allow-Headers').split(', ').sort()
		others = 'Content-Type, Content-Length'.split(', ').sort()
		ASSERT_IS_EQUAL(headers, others)
		ASSERT_IS_EQUAL(response.body['qs'], qs)
		ASSERT_IS_EQUAL(response.body['body'], body)
		return
