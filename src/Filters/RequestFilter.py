# -*- coding: utf-8 -*-

from ..Request import Request
from ..Response import Response

from abc import ABCMeta, abstractmethod

from typing import Tuple, Optional

__all__ = (
	'RequestFilter',
)


class RequestFilter(metaclass=ABCMeta):
	"""Request Filter Interface"""
	@abstractmethod
	def __call__(self, request: Request) -> Tuple[Request, Optional[Response]]:
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
