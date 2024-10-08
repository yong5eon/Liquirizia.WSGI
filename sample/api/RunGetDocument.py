# -*- coding: utf-8 -*-

from Liquirizia.WSGI import Request, RequestProperties
from Liquirizia.WSGI.Properties import RequestRunner
from Liquirizia.WSGI.Responses import *

from Liquirizia.WSGI import Router
from Liquirizia.WSGI.Documentation import Information, Contact

__all__ = (
	'RunGetDocument'
)

@RequestProperties(
	method='GET',
	url='/api/doc',
)
class RunGet(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return

	def run(self):
		return ResponseJSON(Router().toDocument(info=Information(
			title='Liquirizia WSGI Sample API Document',
			version=open('VERSION').read(),
			summary='Liquirizia WSGI Sample API Document',
			description='Liquirizia WSGI Sample API Document',
			contact=Contact(
				name='Liquirizia',
				url='https://www.Liquirizia.com',
				email='contact@Liquirizia.com'
			)
		)))
