# -*- coding: utf-8 -*-

from Liquirizia.Test import *

from webtest import TestApp

from Liquirizia.WSGI import (
		Application, 
		Configuration,
)

from Liquirizia.WSGI import Request, RequestProperties
from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI.Responses import *


@RequestProperties(
	method='GET',
	url='/'
)
class RunGet(RequestRunner):
	def __init__(self, request):
		self.request = request
		return
	def run(self):
		return ResponseOK()


class TestGet(Case):
	@Order(0)
	def testGet(self):
		tester = TestApp(Application(conf=Configuration()), extra_environ={'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': '0'})
		response = tester.get('/')
		return