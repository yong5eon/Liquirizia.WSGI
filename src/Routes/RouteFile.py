# -*- coding: utf-8 -*-

from ..Route import Route
from ..RouteRun import RouteRun

from ..Request import Request
from ..Filters import (
	RequestFilter,
	ResponseFilter,
)
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter
from ..CORS import CORS

from ..Responses import (
	ResponseFile,
	ResponseNotModified,
)

from ..Utils import DateToTimestamp

from email.utils import formatdate
from mimetypes import guess_type
from hashlib import sha1
from os import stat
from os.path import split

__all__ = (
	'RouteFile'
)


class RouteFile(Route, RouteRun):
	"""File Route Class"""

	def __init__(
		self,
		url,
		path,
		onRequest: RequestFilter = None,
		onResponse: ResponseFilter = None,
		cors: CORS = CORS(),
	):
		super(RouteFile, self).__init__('GET', url, cors=cors)
		self.onRequest = onRequest
		self.onResponse = onResponse
		self.path = path
		self.format, self.charset = guess_type(self.path)
		return

	def timestamp(self):
		stats = stat(self.path)
		if not stats:
			raise RuntimeError('cannot read {} file stats'.format(self.path))
		return DateToTimestamp(formatdate(stats.st_mtime, usegmt=True))

	def modified(self):
		stats = stat(self.path)
		if not stats:
			raise RuntimeError('cannot read {} file stats'.format(self.path))
		return formatdate(stats.st_mtime, usegmt=True)

	def etag(self):
		head, tail = split(self.path)
		stats = stat(self.path)
		if not stats:
			raise RuntimeError('cannot read {} file stats'.format(self.path))
		etag = '%d:%d:%d:%d:%s'.format(stats.st_dev, stats.st_ino, stats.st_mtime, stats.st_size, tail)
		return sha1(etag.encode('utf-8')).hexdigest()

	def size(self):
		stats = stat(self.path)
		if not stats:
			raise RuntimeError('cannot read {} file stats'.format(self.path))
		return stats.st_size

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		if self.onRequest:
			request, response = self.onRequest(request)
			if response:
				writer.response(response)
				return

		if request.header('ETag') and request.header('ETag') == self.etag():
			response = ResponseNotModified()
			for k, v in self.headers(request).items():
				response.header(k, v)
			writer.response(response)
			return

		if request.header('If-Modified-Since'):
			timestamp = DateToTimestamp(request.header('If-Modified-Since'))
			if timestamp and timestamp >= self.timestamp():
				response = ResponseNotModified()
				for k, v in self.headers(request).items():
					response.header(k, v)
				writer.response(response)
				return

		# TODO : do cache instead of origin

		offset, size = None, None
		if request.header('Range'):
			offset, end = ParseRange(request.header('Range'), self.size())
			size = end - offset
		else:
			size = self.size()

		response = ResponseFile(file=self.path, offset=offset, size=size)

		if self.onResponse:
			response = self.onResponse.run(response)

		writer.response(response)
		return
