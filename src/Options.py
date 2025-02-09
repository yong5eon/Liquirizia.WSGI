# -*- coding: utf-8 -*-

from .Request import Request
from .Properties import RequestRunner
from .Router import Router
from .CORS import CORS
from .Errors import *
from .Responses import *

__all__ = (
	'Options'
)


class Options(RequestRunner):
	def __init__(self, request: Request):
		self.request = request
		return
	def run(self):
		router = Router()
		if self.request.uri == '*': 
			return ResponseNoContent(headers={
				'Allow': ', '.join(sorted(list(set(router.methods))))
			})
		patterns = router.matches(self.request.uri)
		if not patterns:
			raise NotFoundError('{} is not found in router'.format(self.request.uri))
		# TODO : Use ResponseOK in HTTP/1.0
		response = ResponseNoContent(headers={
			'Allow': ', '.join(patterns.keys()),
			'Access-Control-Allow-Methods': ', '.join(patterns.keys()),
		})
		cors = CORS()
		for _, match in patterns.items():
			if match.route.cors.origin: cors.origin.extend(match.route.cors.origin)
			if match.route.cors.headers: cors.headers.extend(match.route.cors.headers)
			if match.route.cors.credentials: cors.credentials = match.route.cors.credentials
			if match.route.cors.exposeHeaders: cors.exposeHeaders.extend(match.route.cors.exposeHeaders)
			if match.route.cors.age and match.route.cors.age > cors.age: cors.age = match.route.cors.age
		for k, v in cors.toHeaders().items(): response.header(k, v)
		return response
