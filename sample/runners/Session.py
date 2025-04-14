# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Auth import Authenticate
from dataclasses import dataclass

__all__ = (
	'Session',
	'GetSession',
)

@dataclass
class Session(object):
	credentials: str
	extra: dict = None


class GetSession(Authenticate):
	def __call__(self, credentials: str):
		if credentials != '1':
			return
		return Session(
			credentials=credentials,
			extra={
				'id': 0,
			},
		)
