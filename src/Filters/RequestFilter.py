# -*- coding: utf-8 -*-

from ..Request import Request
from ..Response import Response

from abc import ABCMeta, abstractmethod
from typing import Tuple 

__all__ = (
	'RequestFilter',
)


class RequestFilter(metaclass=ABCMeta):
	"""Request Filter Interface"""
	@abstractmethod
	def run(self, request: Request) -> Tuple[Request, Response]:
		raise NotImplementedError('{} must be implemented run'.format(self.__class__.__name__))
