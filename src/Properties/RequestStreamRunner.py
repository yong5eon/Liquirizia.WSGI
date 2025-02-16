# -*- coding: utf-8 -*-

from .Properties import Properties

from ..Request import Request
from ..RequestReader import RequestReader
from ..ResponseWriter import ResponseWriter

from abc import ABCMeta, abstractmethod

__all__ = (
	'RequestStreamRunner',
)


class RequestStreamRunner(metaclass=ABCMeta):
	"""Request Stream Runner Interface for Stream"""

	__properties__: Properties = None

	@abstractmethod
	def __init__(self, request: Request):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))

	@abstractmethod
	def run(self, reader: RequestReader, writer: ResponseWriter):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
