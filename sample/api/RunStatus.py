# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI import RequestProperties
from Liquirizia.WSGI.Description import *
from Liquirizia.WSGI import Request
from Liquirizia.WSGI.Responses import *

from .Format import *

__all__ = (
	'RunStatus'
)


@RequestProperties(
	method='GET',
	url='/',
)
class RunGet(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseOK()
