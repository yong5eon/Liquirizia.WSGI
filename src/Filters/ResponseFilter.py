# -*- coding: utf-8 -*-

from ..Request import Request
from ..Response import Response

from abc import ABCMeta, abstractmethod

__all__ = (
	'ResponseFilter',
)


class ResponseFilter(metaclass=ABCMeta):
	"""Request Filter Interface"""

	@abstractmethod
	def __call__(self, request: Request, response: Response) -> Response:
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
