# -*- coding: utf-8 -*-

from ..Response import Response

from abc import ABCMeta, abstractmethod

__all__ = (
	'ResponseFilter',
)


class ResponseFilter(metaclass=ABCMeta):
	"""Request Filter Interface"""

	@abstractmethod
	def run(self, response: Response) -> Response:
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
