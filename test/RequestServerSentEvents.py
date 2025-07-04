# -*- coding: utf-8 -*-

from Liquirizia.Test import *
from Liquirizia.WSGI.Test import TestRequest, TestRequestServerSentEvents

from Liquirizia.WSGI import (
	Application, 
	Request,
)
from Liquirizia.WSGI.Properties import RequestServerSentEventsRunner, RequestServerSentEventsProperties
from Liquirizia.WSGI.Responses import *
from Liquirizia.WSGI.Extends import ServerSentEvents

from time import sleep
from random import randrange


@RequestServerSentEventsProperties(
	method='GET',
	url='/sse',
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


class RequestServerSentEvents(Case):
	@Order(0)
	def testOptions(self):
		_ = TestRequest(Application())
		response = _.request(
			method='OPTIONS',
			uri='*'
		)
		ASSERT_TRUE(response.status in (200, 204))
		ASSERT_TRUE('GET' in response.header('Allow'))
		response = _.request(
			method='OPTIONS',
			uri='/sse'
		)
		ASSERT_TRUE(response.status in (200, 204))
		ASSERT_TRUE('GET' in response.header('Allow'))
		return

	@Order(1)
	def testRequest(self):
		_ = TestRequestServerSentEvents(Application())
		response = _.request(
			method='GET',
			uri='/sse',
		)
		ASSERT_IS_EQUAL(response.status, 200)
		ASSERT_IS_EQUAL(response.header('Content-Type').format, 'text/event-stream')
		for idx, event in enumerate(response.events()):
			ASSERT_IS_EQUAL(event.data, str(idx))
			ASSERT_IS_EQUAL(event.id, str(idx))
			ASSERT_IS_EQUAL(event.event, None)
		return
