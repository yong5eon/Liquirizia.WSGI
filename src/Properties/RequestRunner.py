# -*- coding: utf-8 -*-

from ..Request import Request

from abc import ABCMeta, abstractmethod

__all__ = (
	'RequestRunner',
)


class RequestRunner(metaclass=ABCMeta):
	"""Request Runner Interface"""

	@abstractmethod
	def __init__(self, request: Request):
		raise NotImplementedError('{} must be implemented __init__'.format(self.__class__.__name__))

	@abstractmethod
	def run(self):
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
