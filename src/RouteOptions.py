# -*- coding: utf-8 -*-

from .RouteRun import RouteRun
from .Request import Request
from .RequestReader import RequestReader
from .ResponseWriter import ResponseWriter

from .Options import Options

__all__ = (
	'RouteOptions'
)


class RouteOptions(RouteRun):
	"""Route Options Class"""
	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		obj = Options(request)
		response = obj.run()
		writer.response(response)
		return
