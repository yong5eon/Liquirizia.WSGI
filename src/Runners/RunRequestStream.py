# -*- coding: utf-8 -*-

from ..Route import Route
from ..RequestFactory import RequestFactory
from ..Request import Request
from ..Properties import RequestStreamRunner
from ..Validators import (
	Origin,
	Auth,
	Parameter,
	QueryString,
	Header,
	Body,
)
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter

from typing import Type

__all__ = (
	'RunRequestStream'
)


class RunRequestStream(Route, RequestFactory):
	"""Run Request Stream Class"""
	def __init__(
		self,
		obj: Type[RequestStreamRunner],
		method: str,
		url: str,
		origin: Origin = None,
		auth: Auth = None,
		parameter: Parameter = None,
		qs: QueryString = None,
		header: Header = None,
	):
		super().__init__(method, url)
		self.object = obj
		self.origin = origin
		self.auth = auth
		self.parameter = parameter
		self.qs = qs
		self.header = header
		return

	def run(
		self,
		request: Request,
		reader: RequestReader,
		writer: ResponseWriter,
	):
		if self.origin: self.origin(request)
		if self.auth: self.auth(request)
		if self.parameter: self.parameter(request)
		if self.qs: self.qs(request)
		if self.header: self.header(request)
		o = self.object(request)
		o.run(reader, writer)
		return
