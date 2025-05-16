# -*- coding: utf-8 -*-

from Liquirizia.WSGI.Errors.ClientError import UnauthorizedError
from Liquirizia.WSGI.Validators import Authorization
from dataclasses import dataclass

__all__ = (
	'Session',
	'GetSession',
)

@dataclass
class Session(object):
	credentials: str
	extra: dict = None


class GetSession(Authorization):
	def __call__(self, credentials: str):
		if credentials != '1':
			raise UnauthorizedError(reason='Invalid credentials')
		return Session(
			credentials=credentials,
			extra={
				'id': 0,
			},
		)
