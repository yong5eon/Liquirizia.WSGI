# -*- coding: utf-8 -*-

from .RouteRun import RouteRun
from .Request import Request
from .RequestReader import RequestReader
from .ResponseWriter import ResponseWriter
from .Errors import BadRequestError, UnsupportedMediaTypeError

from .Options import Options

from Liquirizia.Serializer import SerializerHelper
from Liquirizia.Serializer.Errors import NotSupportedError, DecodeError

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
		if request.size:
			try:
				request.body = SerializerHelper.Decode(
					reader.read(request.size),
					format=request.format,
					charset=request.charset,
				)
			except NotSupportedError as e:
				raise UnsupportedMediaTypeError(str(e), error=e)
			except DecodeError as e:
				raise BadRequestError(str(e), error=e)

		obj = Options(request)
		response = obj.run()

		writer.response(response)
		return
