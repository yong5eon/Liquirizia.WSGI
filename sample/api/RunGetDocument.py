# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Properties import RequestProperties, RequestRunner
from Liquirizia.WSGI import Request
from Liquirizia.WSGI.Responses import *

from Liquirizia.WSGI.Description import Descriptor, Tag

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
		return ResponseJSON(Descriptor().toDocument(tags=(
			Tag('RequestRunner'),
			Tag('RequestRunner - Content Validation'),
			Tag('RequestStreamRunner'),
			Tag('RequestStreamRunner - Chunked'),
			Tag('RequestServerSentEventsRunner'),
			Tag('RequestWebSocketRunner'),
		)))
