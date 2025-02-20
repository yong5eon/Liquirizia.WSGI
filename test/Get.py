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

from Liquirizia.WSGI.Test import TestRequest

from dataclasses import asdict


@RequestProperties(
	method='GET',
	url='/',
)
class RunGet(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self) -> Response:
		return ResponseJSON(asdict(self.request.qs))


class TestGet(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='OPTIONS',
			uri='*'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_IS_EQUAL('GET' in response.header('Allow'), True)
		response = _.request(
			method='OPTIONS',
			uri='/'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_IS_EQUAL('GET' in response.header('Allow'), True)
		return

	@Parameterized(
			{'qs': {'a': '1', 'b': '3'}},
	)
	@Order(1)
	def testRequest(self, qs):
		_ = TestRequest(Application(conf=Configuration()))
		response = _.request(
			method='GET',
			uri='/',
			qs=qs,
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_IS_EQUAL(response.body, qs)
		return
