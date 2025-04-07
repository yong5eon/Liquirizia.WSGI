# -*- coding: utf-8 -*-

from ..RequestFactory import RequestFactory
from ..Request import Request
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..Router import Router
from ..Errors import *
from ..Responses import *


__all__ = (
	'RouteOptions'
)


class RouteOptions(RequestFactory):
	"""Route Options Class"""
	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		router = Router()
		if request.uri == '*': 
			return ResponseNoContent(headers={
				'Allow': ', '.join(sorted(list(set(router.methods))))
			})
		_, patterns = router.matches(self.request.uri)
		if not patterns:
			raise NotFoundError('{} is not found in router'.format(self.request.uri))
		# TODO : Use ResponseOK in HTTP/1.0
		response = ResponseNoContent(headers={
			'Allow': ', '.join(patterns.keys()),
			'Access-Control-Allow-Methods': ', '.join(patterns.keys()),
		})
		writer.response(response)
		return
