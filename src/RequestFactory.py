# -*- coding: utf-8 -*-

from .Request import Request
from .Response import Response

from .RequestReader import RequestReader
from .ResponseWriter import ResponseWriter

from abc import ABCMeta, abstractmethod

__all__ = (
	'RequestFactory'
)


class RequestFactory(metaclass=ABCMeta):
	"""RequestFactory Interface"""
	@abstractmethod
	def run(self, request: Request, reader: RequestReader, writer: ResponseWriter) -> Response:
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
