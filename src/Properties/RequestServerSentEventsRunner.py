# -*- coding: utf-8 -*-

from ..Request import Request
from ..Extends import ServerSentEvents

from abc import ABCMeta, abstractmethod

__all__ = (
	'RequestServerSentEventsRunner',
)


class RequestServerSentEventsRunner(metaclass=ABCMeta):
	"""Request Server Sent Events Runner Interface for Stream"""
	@abstractmethod
	def __init__(self, request: Request):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))

	@abstractmethod
	def run(self, writer: ServerSentEvents):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
