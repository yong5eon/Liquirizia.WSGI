# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from Liquirizia.WSGI import (
		Application, 
		Configuration,
		CORS,
)

from Liquirizia.WSGI import Request, Response, Error
from Liquirizia.WSGI.Properties import RequestRunner, RequestProperties
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Errors import *

from Liquirizia.WSGI.Test import TestRequest


@RequestProperties(
	method='GET',
	url='/error',
)
class RunError(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self) -> Response:
		raise BadRequestError(
			'잘못된 요청',
			headers={
				'X-Error-Code': 1,
				'X-Error-Message': 'Reason',
			},
			body='Bad Request'.encode('utf-8'),
			format='text/plain',
			charset='utf-8',
		)


class TestError(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='OPTIONS',
			uri='*'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_TRUE('GET' in response.header('Allow'))
		response = _.request(
			method='OPTIONS',
			uri='/error'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_TRUE('GET' in response.header('Allow'))
		return

	@Parameterized(
			{'qs': {'a': '1', 'b': '3'}},
	)
	@Order(1)
	def testRequest(self, qs):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='GET',
			uri='/error',
			qs=qs,
		)
		ASSERT_IS_EQUAL(response.status, 400)
		ASSERT_IS_EQUAL(response.header('X-Error-Code'), '1')
		ASSERT_IS_EQUAL(response.header('X-Error-Message'), 'Reason')
		ASSERT_IS_EQUAL(response.body, 'Bad Request')
		return
