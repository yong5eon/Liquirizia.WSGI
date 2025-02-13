# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Test import TestRequest, TestRequestServerSentEvents

from Liquirizia.WSGI import (
	Application, 
	Configuration,
	CORS,
	RequestProperties,
	Request,
)
from Liquirizia.WSGI.Properties import RequestServerSentEventsRunner
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Extends import ServerSentEvents

from time import sleep
from random import randrange


@RequestProperties(
	method='GET',
	url='/sse',
	cors=CORS()
)
class RunGetServerSentEvents(RequestServerSentEventsRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self, writer: ServerSentEvents):
		writer.begin()
		for i in range(0, 10):
			writer.emit(data=str(i), id=str(i))
			sleep(0.1)
		writer.end()
		return


class TestGetServerSentEvents(Case):
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
			uri='/sse'
		)
		ASSERT_IS_EQUAL(response.status, 204)
		ASSERT_TRUE('GET' in response.header('Allow'))
		return

	@Order(1)
	def testRequest(self):
		_ = TestRequestServerSentEvents(Application(conf=Configuration()))
		response = _.request(
			method='GET',
			uri='/sse',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_IS_EQUAL(response.header('Content-Type').type, 'text/event-stream')
		for idx, event in enumerate(response.events()):
			ASSERT_IS_EQUAL(event.data, str(idx))
			ASSERT_IS_EQUAL(event.id, str(idx))
			ASSERT_IS_EQUAL(event.event, None)
		return
